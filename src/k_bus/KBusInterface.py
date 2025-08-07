import serial
import time

from serial.serialutil import PARITY_EVEN, STOPBITS_ONE


# K-Bus Message format:
# LSB first, MSB last
# Low Start of Message bit
# Message Data
# Even Parity Bit
# High End of Message
class KbusSerial:
    def __init__(self, port):
        self.ser = serial.Serial(port=port, baudrate=9600, parity=PARITY_EVEN, stopbits=STOPBITS_ONE, rtscts=True)
        self.cts = self.ser.rtscts

    def tx(self, cmd):
        while True:
            print("loop")
            if self.cts:
                self.ser.write(cmd)
                print("Sent")
                break

    def rx(self):
        pass

    def terminate(self):
        self.ser.close()
