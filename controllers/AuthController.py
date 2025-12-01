from services.AuthService import AuthService
from ui import EmployeeMainWindow
from ui.login.LoginWindow import LoginWindow
from ui.admin.mainWindow import ParkingManagementApp
import sys
from PyQt6.QtWidgets import QApplication

class AuthController:
    def __init__(self, app: QApplication):
        self.app = app
        self.auth_service = AuthService()
        self.login_window = LoginWindow()
        self.main_window = None

        self.login_window.login_btn.clicked.connect(self.handle_login)

    def show_login_window(self):
        self.login_window.show()

    def handle_login(self):
        username, password = self.login_window.get_username_password_input()
        staff = self.auth_service.login(username, password)

        if staff and staff.role == 1:
            self.show_admin_window()
        elif staff and staff.role == 2:
            self.show_employee_window()
        else:
            LoginWindow.show_error("Sai tài khoản hoặc mật khẩu!")

    def show_admin_window(self):
        self.login_window.close()
        self.main_window = ParkingManagementApp()
        self.main_window.show()

    def show_employee_window(self):
        self.login_window.close()
        self.main_window = EmployeeMainWindow()
        self.main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth = AuthController(app)
    auth.show_login_window()
    sys.exit(app.exec())
