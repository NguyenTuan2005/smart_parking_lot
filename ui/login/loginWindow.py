from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đăng nhập hệ thống")
        # Đảm bảo cửa sổ đủ lớn để chứa nội dung
        self.setGeometry(500, 200, 400, 300)
        self.setStyleSheet("background-color: #f0f2f5;")
        self.accept_login = False
        self.user_type = None
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
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 10px;
                padding-left: 10px;
                font-size: 14px;
                color: #333; /* Đảm bảo màu chữ là tối trên nền sáng */
            }
            QLineEdit:focus {
                border: 2px solid #2E86C1;
            }
        """)
        layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 10px;
                padding-left: 10px;
                font-size: 14px;
                color: #333; /* Đảm bảo màu chữ là tối trên nền sáng */
            }
            QLineEdit:focus {
                border: 2px solid #2E86C1;
            }
        """)
        layout.addWidget(self.password_input)

        # Nút đăng nhập
        login_btn = QPushButton("Đăng nhập")
        login_btn.setFixedHeight(40)
        login_btn.setStyleSheet("""
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
        login_btn.clicked.connect(self.check_login)
        layout.addWidget(login_btn)

        # Ghi chú
        note = QLabel("Admin: admin/12345 | User: user/user")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setStyleSheet("color: #555; font-size: 12px;")  # Màu chữ tối, sẽ hiển thị
        layout.addWidget(note)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "12345":
            self.accept_login = True
            self.user_type = "admin"
            self.close()
        elif username == "user" and password == "user":
            self.accept_login = True
            self.user_type = "user"
            self.close()
        else:
            # Sửa lỗi màu chữ trong QMessageBox
            msg = QMessageBox(self)
            msg.setWindowTitle("Lỗi Đăng nhập")
            msg.setText("Tên đăng nhập hoặc mật khẩu không đúng!")
            msg.setIcon(QMessageBox.Icon.Warning)

            # Áp dụng Style Nền Tối và Chữ Sáng cho QMessageBox (nhất quán với theme chính)
            msg.setStyleSheet("""
                QMessageBox { background-color: #34495e; } 
                QLabel { color: #ecf0f1; } 
                QPushButton {
                    background-color: #e74c3c; 
                    color: white;
                    border-radius: 4px;
                    padding: 5px 10px;
                }
                QPushButton:hover { background-color: #c0392b; }
            """)
            # Thay thế exec_() bằng exec() cho PyQt6
            msg.exec()