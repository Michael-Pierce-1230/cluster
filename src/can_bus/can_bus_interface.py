import can



class CanBusInterface:

    def __init__(self, channel, bus_type):
        # setup interface
        # bus_types:
        #   - virtual
        #   - slcan (serial lin can)
        #   - socketcan (linux kernal CAN driver: vcan, can0, etc)

        self.bus = can.interface.Bus(channel=channel, interface=bus_type)

    def tx_can_msg(self, can_id, data):

        msg = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)

        try:
            self.bus.send(msg)
        except can.CanError:
            print("Message NOT Sent")

    def rx_can_msg(self):
        pass