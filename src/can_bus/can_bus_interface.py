import time

import can
import cantools
import os



class CanBusInterface:

    def __init__(self, channel, bus_type):
        # setup interface
        # bus_types:
        #   - virtual
        #   - slcan (serial lin can)
        #   - socketcan (linux kernal CAN driver: vcan, can0, etc)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        dbc_path = os.path.join(current_dir, "instrument_cluster.dbc")
        self.db = cantools.database.load_file(dbc_path)
        # for message in db.messages:
        #     print(f"  - Message Name: {message.name}, ID: {hex(message.frame_id)}")


        self.bus = can.interface.Bus(channel=channel, interface=bus_type)

    def tx_can_msg(self, can_id, data):

        msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

        try:
            self.bus.send(msg)
        except can.CanError:
            print("Message NOT Sent")

    def rx_can_msg(self):
        msg = self.bus.recv(timeout=1)
        if msg is not None:
            print(f"message ID {msg.arbitration_id}")
            print(self.db.decode_message(msg.arbitration_id, msg.data))

if __name__ == "__main__":

    CI = CanBusInterface("vcan0", "socketcan")
    for i in range(10):
        CI.rx_can_msg()
        time.sleep(1)

    print("can")