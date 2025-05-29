from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
from rfid_reader import RFIDReader
from schemas import RFIDEvent
import asyncio

app = FastAPI()
reader = RFIDReader('/dev/serial0', 9600)
clients = set()
event_counter = 0
reading = False

@app.post("/cloud/start")
async def start_reading():
    global reading
    if reading:
        return {"status": "already_started"}
    
    reading = True
    asyncio.create_task(read_loop())
    return {"status": "started"}

@app.post("/cloud/stop")
async def stop_reading():
    global reading
    reading = False
    return {"status": "stopped"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep alive (optional)
    except WebSocketDisconnect:
        clients.remove(websocket)

async def broadcast(event: RFIDEvent):
    message = event.model_dump_json()
    for client in clients:
        await client.send_text(message)

async def read_loop():
    global event_counter
    while reading:
        tag = reader.read_tag()
        if tag:
            event_counter += 1
            event = RFIDEvent(
                data={
                    "eventNum": event_counter,
                    "format": "epc",
                    "idHex": tag.upper()
                },
                timestamp=datetime.now().isoformat(),
                type="CUSTOM"
            )
            await broadcast(event)
        await asyncio.sleep(0.1)
