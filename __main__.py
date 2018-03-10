import sys
from PyQt4 import QtGui

from egps_window import EGPSWindow

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    GUI = EGPSWindow()
    sys.exit(app.exec_())
