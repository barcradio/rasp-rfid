# RFID Reader Architecture - Raspberry Pi Bridge

## Overview
This design describes how to connect a **serial-only RFID reader** (Shenzhen RFIDSU) to a **Raspberry Pi**, and expose two key interfaces for external clients:

- **HTTP (REST API)**: Used to configure the reader (start/stop scanning, set parameters, etc.)
- **WebSocket**: Used to broadcast real-time tag reads to clients.

---
## Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
---
## System Diagram

```
+---------------------------------------+
|                 Client                |
| (Browser / Dashboard / Control App)   |
|                                       |
| 1. HTTP: Configure Reader (REST API)  |
| 2. WebSocket: Receive Tag Scans       |
+---------------------------------------+
                |
                |
      (Over Local Network or WiFi)
                |
+---------------------------------------+
|             Raspberry Pi              |
|                                       |
| +-------------------------------+    |
| | RFID Serial Reader Interface   |    |
| | - Reads EPC from serial port   |    |
| | - Handles reader commands      |    |
| +-------------------------------+    |
|               |                       |
| +-------------------------------+    |
| | HTTP Server (REST API)        |    |
| | - Set reader mode (scan/idle)  |    |
| | - Query reader status          |    |
| | - Configure parameters         |    |
| +-------------------------------+    |
|               |                       |
| +-------------------------------+    |
| | WebSocket Server              |    |
| | - Broadcasts tag reads        |    |
| | - Clients subscribe for live  |
| |   tag data                    |
| +-------------------------------+    |
+---------------------------------------+
                |
      (Connected via Serial)
                |
+---------------------------------------+
|        RFID Reader (Serial)           |
|  (Shenzhen RFIDSU, ISO18000-6C)       |
|                                       |
| Scans tags --> Sends EPC via Serial   |
| Receives config commands via Serial   |
+---------------------------------------+
```

---

## Summary of Roles

| Component          | Role |
|----------------|----------------------------|
| **RFID Reader** | Scans tags, sends tag data over serial, accepts configuration commands over serial |
| **Raspberry Pi** | Acts as a middleware — handles serial communication, provides configuration via HTTP, streams live tag data via WebSocket |
| **Client App** (Browser, Dashboard, etc.) | Configures the reader (via HTTP) and receives real-time tag data (via WebSocket) |

---

## Protocols in Use

| Protocol   | Purpose |
|------------|---------------------|
| **HTTP (REST)** | Configure and control the reader (start/stop scanning, set power level, etc.) |
| **WebSocket** | Broadcasts live tag reads to connected clients |
| **Serial (UART)** | Direct communication between Pi and RFID reader |

---

## Example Data Flow - Tag Scan

1. RFID reader scans a tag.
2. Reader sends EPC over **serial** to Raspberry Pi.
3. Raspberry Pi parses the serial message into structured **JSON**.
4. Pi broadcasts this JSON to all **WebSocket clients**.
5. Any connected client (dashboard, mobile app, etc.) instantly receives the tag event.

---

## Example Data Flow - Configuration

1. Client wants to **start a scan session**.
2. Client sends `POST /api/start-scan` to the Pi’s HTTP server.
3. Pi sends the corresponding **serial command** to the reader.
4. Reader begins scanning and sending tag data.
5. Tags appear on the client via **WebSocket**.

---

## Example Serial Data from Reader

*(This part depends on the actual reader, but you might see something like:)*

```
SOH <EPC_HEX> <TIMESTAMP> <CRC>
```

---

## Future Enhancements

- Add secure authentication to the HTTP and WebSocket interfaces.
- Add more advanced configuration options (scan intervals, power levels, antenna tuning).
- Optionally store tag scan events into a database for historical reporting.
- Add remote firmware update capabilities for the reader.

---

End of Document

