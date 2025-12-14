from controllers.AuthController import AuthController
from services.AuthService import AuthService
from services.Session import Session
from ui import EmployeeMainWindow
from ui.login.LoginWindow import LoginWindow
from ui.admin.mainWindow import ParkingManagementApp
import sys
from PyQt6.QtWidgets import QApplication

class AppController:
    def __init__(self):
        self.auth_controller = AuthController()
        self.login_window = LoginWindow()
        self.main_window = None
        self.login_window.login_requested.connect(self.handle_login)


    def show_login_window(self):
        self.login_window.show()

    def handle_login(self, username, password):
        user = self.auth_controller.authenticate(username, password)

        if not user:
            self.login_window.show_error("Sai tài khoản hoặc mật khẩu")
            return

        Session.login(user)

        self.login_window.close()

        if user.role == 1:
            self.show_admin_window()
        elif user.role == 2:
            self.show_employee_window()

    def show_admin_window(self):
        self.login_window.close()
        self.main_window = ParkingManagementApp()
        self.main_window.logout_requested.connect(self.logout)
        self.main_window.show()

    def show_employee_window(self):
        self.login_window.close()
        self.main_window = EmployeeMainWindow()
        self.main_window.logout_requested.connect(self.logout)
        self.main_window.show()

    def logout(self):
        Session.logout()

        if self.main_window:
            self.main_window.close()
            self.main_window = None
        self.login_window.show()

    def start(self):
        self.login_window.show()