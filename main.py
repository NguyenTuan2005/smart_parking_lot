"""
Main entry point for Smart Parking Lot Management System
Handles login and role-based routing to admin or employee interface
"""
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

from controllers.AppController import AppController
from ui.login import LoginWindow
from ui.admin import ParkingManagementApp
from ui.employee import EmployeeMainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth = AppController()
    auth.show_login_window()
    sys.exit(app.exec())

