from PyQt5.QtWidgets import QMainWindow
import E46_BCM
import KBusInterface
import KBusMsgs

kbus = KBusInterface.KbusSerial('COM1')
class E46Window(QMainWindow, E46_BCM.Ui_MainWindow):

    def runFDClose(self):
        print("Close front Driver Window")
        kbus.tx(KBusMsgs.FDWClose)

    def runRDClose(self):
        print("Close Rear Driver Window")
        kbus.tx(KBusMsgs.IntLights)

    def runFDOpen(self):
        print("Open front Driver Window")
        kbus.tx(KBusMsgs.FDWOpen)

    def runRDOpen(self):
        print("Open Rear Driver Window")
        #kbus.tx(KBusMsgs.RDWOpen)

    def runFPClose(self):
        print("Close front Passenger Window")
        kbus.tx(KBusMsgs.FPWClose)

    def runRPClose(self):
        print("Close Rear Passenger Window")
        #kbus.tx(KBusMsgs.RPWClose)

    def runFPOpen(self):
        print("Open front Passenger Window")
        kbus.tx(KBusMsgs.FPWOpen)

    def runRPOpen(self):
        print("Open Rear Passenger Window")
        #kbus.tx(KBusMsgs.RPWClose)

    def runLocks(self):
        print("Lock/ Unlock")
        kbus.tx(KBusMsgs.lock)


    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        # Driver side windows
        self.FDClose.clicked.connect(self.runFDClose)
        self.FDOpen.clicked.connect(self.runFDOpen)
        self.RDClose.clicked.connect(self.runRDClose)
        self.RDOpen.clicked.connect(self.runRDOpen)

        # Passenger side windows
        self.FPClose.clicked.connect(self.runFPClose)
        self.FPOpen.clicked.connect(self.runFPOpen)
        self.RPClose.clicked.connect(self.runRPClose)
        self.RPOpen.clicked.connect(self.runRPOpen)

        # Interior Lock Switch
        self.LockSwitch.clicked.connect(self.runLocks)
