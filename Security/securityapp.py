from PyQt5.QtWidgets import QApplication
from Security.mainframe import MainDialog
import sys


class SecurityApp(QApplication):
    def __init__(self):
        super(SecurityApp, self).__init__(sys.argv)
        self.dialog = MainDialog()
        self.dialog.show()
