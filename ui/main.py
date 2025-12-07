"""
Main entry point for Smart Parking Lot Management System
Handles login and role-based routing to admin or employee interface
"""
import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

from controllers.AuthController import AuthController
from ui.login import LoginWindow
from ui.admin import ParkingManagementApp
from ui.employee import EmployeeMainWindow

def main():
    app = QApplication(sys.argv)


    # Event loop chính
    while True:
        # Show login window
        login_window = LoginWindow()
        login_window.exec()

        # Check if login was successful
        if not login_window.accept_login:
            sys.exit(0)  # Exit if login failed or was cancelled

        # Route to appropriate window based on user type
        if login_window.user_type == "admin":
            # Open admin interface
            admin_window = ParkingManagementApp()

            # Connect logout signal để quay lại login
            admin_window.logout_signal.connect(lambda: None)

            admin_window.show()
            app.exec()

            # Nếu admin đăng xuất, vòng lặp tiếp tục để hiển thị login lại

        elif login_window.user_type == "user":
            # Open employee interface
            employee_window = EmployeeMainWindow()

            # Connect logout signal để quay lại login
            employee_window.logout_signal.connect(lambda: None)

            employee_window.show()
            app.exec()

            # Nếu employee đăng xuất, vòng lặp tiếp tục để hiển thị login lại
        else:
            QMessageBox.critical(None, "Lỗi", "Loại người dùng không hợp lệ!")
            sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth = AuthController(app)
    auth.show_login_window()
    sys.exit(app.exec())

    # main()
