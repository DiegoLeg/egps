import sys
from PyQt4 import QtGui

from window import Window

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
