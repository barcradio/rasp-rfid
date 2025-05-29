# Example stub for schemas.py
from pydantic import BaseModel

class RFIDData(BaseModel):
    eventNum: int
    format: str
    idHex: str

class RFIDEvent(BaseModel):
    data: RFIDData
    timestamp: str
    type: str