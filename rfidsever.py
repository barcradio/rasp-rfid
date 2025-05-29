# Example stub for rfid_reader.py
class RFIDReader:
    def __init__(self, port: str, baudrate: int):
        import serial
        self.ser = serial.Serial(port, baudrate, timeout=0.1)

    def read_tag(self) -> str:
        if self.ser.in_waiting:
            data = self.ser.read(self.ser.in_waiting)
            hex_data = data.hex()
            if len(hex_data) >= 23:  # Adjust based on actual data length
                return hex_data[4:27]  # Example slicing, adjust per device spec
        return ""


