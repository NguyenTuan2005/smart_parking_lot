"""
Main entry point
"""

import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from controllers.AppController import AppController


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icons/logo.png"))
    auth = AppController()
    auth.show_login_window()
    sys.exit(app.exec())
