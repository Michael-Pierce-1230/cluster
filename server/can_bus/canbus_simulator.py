import can
import time
import random

#Setup virtual CAN Interface
bus = can.interface.Bus(channel='vcan0', interface='socketcan')

# Initial values
rpm = 800
speed = 0
coolant_temp = 40 # Celsius
fuel_level = 100
throttle = 0

def send_can_message(can_id, data):
    msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

    try:
        bus.send(msg)
    except can.canError:
        print("Message NOT sent")

print("CAN simulation server started...")

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

    send_can_message(0x0C0, rpm_bytes)
    send_can_message(0x0C1, speed_bytes)
    send_can_message(0x0C2, coolant_byte)
    send_can_message(0x0C3, fuel_byte)
    send_can_message(0x0C4, throttle_byte)

    time.sleep(0.1)

