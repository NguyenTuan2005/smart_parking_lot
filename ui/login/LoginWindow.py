from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class LoginWindow(QDialog):
    login_requested = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.login_btn = QPushButton("Đăng nhập")

        self.setWindowTitle("Đăng nhập hệ thống")
        self.setGeometry(500, 200, 400, 300)
        self.setStyleSheet("background-color: #f0f2f5;")
        self.initUI()


    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)  # Giảm spacing

        # Tiêu đề
        title = QLabel("HỆ THỐNG QUẢN LÝ BÃI XE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Sửa QFont.Bold -> QFont.Weight.Bold
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2E86C1;")
        layout.addWidget(title)

        # Username
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 10px;
                padding-left: 10px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #2E86C1;
            }
        """)
        layout.addWidget(self.username_input)

        # Password
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 10px;
                padding-left: 10px;
                font-size: 14px;
                color: #333; 
            }
            QLineEdit:focus {
                border: 2px solid #2E86C1;
            }
        """)
        layout.addWidget(self.password_input)

        # Nút đăng nhập
        self.login_btn.setFixedHeight(40)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1;
                color: white;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1B4F72;
            }
        """)
        layout.addWidget(self.login_btn)
        self.login_btn.clicked.connect(self._emit_login)

        self.setLayout(layout)

    def _emit_login(self):
        self.login_requested.emit(
            self.username_input.text(),
            self.password_input.text()
        )

    @staticmethod
    def show_error(message: str):
        msg = QMessageBox()
        msg.setWindowTitle("Login Error")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg.setStyleSheet("""
            QMessageBox {
            
                background-color: white;
                font-size: 14px;
            }
            QLabel { 
                background-color: white;
                color: black;
            }
            QPushButton {
                background-color: white;
                color: black;
                border: 1px solid #1b4f72;
                padding: 5px 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f2f2f2;
            }
        """)

        msg.exec()
