from tabnanny import check

import can
import time
import random
import os
import subprocess

from src.can_bus.can_bus_interface import CanBusInterface
def main():
    #Load vcan module
    subprocess.run(["sudo", "modprobe", "vcan"], check=True)

    # Check if vcan0 already exists
    result = subprocess.run(["ip", "link", "show", "vcan0"], capture_output=True)
    if result.returncode != 0:
        # add vcan0 if it doesnt exist
        subprocess.run(["sudo", "ip", "link", "add", "dev", "vcan0", "type", "vcan"], check=True)

    #bring up vcan0
    subprocess.run(["sudo", "ip", "link", "set", "up", "vcan0"], check=True)
    print("Vcan0 is ready.")

    #Setup virtual CAN Interface
    bus = can.interface.Bus(channel='vcan0', interface='socketcan')

    # Initial values
    rpm = 800
    speed = 0
    coolant_temp = 40 # Celsius
    fuel_level = 100
    throttle = 0

    print("CAN simulation server started...")
    try:
        while True:
            # Simulate driving patterns
            if speed < 60:
                speed += random.randint(0, 2)
                rpm += random.randint(50, 150)
                throttle = min(100, throttle + random.randint(1, 3))
            else:
                speed -= random.randint(0, 2)
                rpm -= random.randint(50, 100)
                throttle = max(0, throttle - random.randint(1, 2))

            # Clamp values
            rpm = max(700, min(rpm, 6000))
            speed = max(0, min(speed, 120))
            throttle = max(0, min(throttle, 100))

            # Coolant warms up then stabilizes
            if coolant_temp < 90:
                coolant_temp += 0.2
            else:
                coolant_temp += random.uniform(-0.2, 0.2)

            # Fuel decreases over time
            if speed > 0 and fuel_level > 0:
                fuel_level -= 0.01

            # prepare msgs (2-byte big-endian where needed)
            rpm_bytes = rpm.to_bytes(2, 'big') # ID 0X0C0
            speed_bytes = speed.to_bytes(2, 'big') # ID 0X0C1
            coolant_byte = int(coolant_temp).to_bytes(1, 'big')  # ID 0X0C2
            fuel_byte = int(fuel_level).to_bytes(1, 'big')  # ID 0X0C3
            throttle_byte = int(throttle).to_bytes(1, 'big')  # ID 0X0C4

            bus.send(can.Message(arbitration_id=0x0C, data=rpm_bytes, is_extended_id=False))
            bus.send(can.Message(arbitration_id=0x0D, data=speed_bytes, is_extended_id=False))
            bus.send(can.Message(arbitration_id=0x05, data=coolant_byte, is_extended_id=False))
            bus.send(can.Message(arbitration_id=0x03, data=fuel_byte, is_extended_id=False))
            bus.send(can.Message(arbitration_id=0x11, data=throttle_byte, is_extended_id=False))
            # bus.tx_can_msg(0x0C1, speed_bytes)
            # bus.tx_can_msg(0x0C2, coolant_byte)
            # bus.tx_can_msg(0x0C3, fuel_byte)
            # bus.tx_can_msg(0x0C4, throttle_byte)

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Shutting down Vcan0")
        bus.shutdown()
        subprocess.run(["sudo", "ip", "link", "set", "vcan0", "down"], check=True)

if __name__ == "__main__":
    main()

