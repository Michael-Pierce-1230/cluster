import serial
import window
from PyQt5 import QtCore, QtGui, QtWidgets
import sys







app = QtWidgets.QApplication(sys.argv)
ui = window.E46Window()
ui.show()
sys.exit(app.exec_())
