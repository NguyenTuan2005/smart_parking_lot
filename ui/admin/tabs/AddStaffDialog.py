from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt


class AddStaffDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thông tin nhân viên")
        self.setFixedSize(420, 280)
        self.is_edit_mode = False  # Biến để phân biệt Thêm/Sửa
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Họ tên *")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Số điện thoại *")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username *")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Nhân viên"])

        for w in [
            self.fullname_input,
            self.phone_input,
            self.username_input,
            self.password_input,
            self.role_combo
        ]:
            w.setFixedHeight(35)
            layout.addWidget(w)

        # ===== BUTTON =====
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Lưu hệ thống")
        self.btn_cancel = QPushButton("Hủy bỏ")

        # Style cho nút bấm
        self.btn_save.setStyleSheet("background-color: #2ECC71; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_cancel.setStyleSheet("background-color: #E74C3C; color: white; font-weight: bold; border-radius: 5px;")

        self.btn_save.setFixedHeight(36)
        self.btn_cancel.setFixedHeight(36)

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)

        # Connect
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.validate_and_accept)

    def set_data(self, fullname, phone, username, role):
        """Dùng khi Chỉnh sửa: Đổ dữ liệu cũ vào form"""
        self.is_edit_mode = True
        self.setWindowTitle("Chỉnh sửa nhân viên")
        self.fullname_input.setText(fullname)
        self.phone_input.setText(phone)
        self.username_input.setText(username)
        # 1: Admin (index 0), 0: Nhân viên (index 1)
        self.role_combo.setCurrentIndex(0 if role == 1 else 1)
        self.password_input.setPlaceholderText("Để trống nếu không đổi mật khẩu")

    def validate_and_accept(self):
        """Kiểm tra dữ liệu trước khi đóng Dialog"""
        fullname = self.fullname_input.text().strip()
        phone = self.phone_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Kiểm tra các trường bắt buộc
        if not all([fullname, phone, username]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ các trường dấu (*)")
            return

        # Nếu là thêm mới (không phải edit) thì bắt buộc nhập password
        if not self.is_edit_mode and not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mật khẩu cho nhân viên mới")
            return

        self.accept()

    def get_data(self):
        """Trả về dictionary để Service xử lý"""
        return {
            "fullname": self.fullname_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),  # Có thể rỗng nếu là Edit
            "role": 1 if self.role_combo.currentText() == "Admin" else 0
        }