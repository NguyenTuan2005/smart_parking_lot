from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt


class AddStaffDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm nhân viên")
        self.setFixedSize(420, 260)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Họ tên")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Số điện thoại")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mật khẩu")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Staff"])

        for w in [
            self.fullname_input,
            self.phone_input,
            self.username_input,
            self.password_input,
            self.role_combo
        ]:
            w.setFixedHeight(32)
            layout.addWidget(w)

        # ===== BUTTON =====
        btn_layout = QHBoxLayout()

        self.btn_save = QPushButton("Lưu")
        self.btn_cancel = QPushButton("Hủy")

        self.btn_save.setFixedHeight(36)
        self.btn_cancel.setFixedHeight(36)

        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)

        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.accept)

    def get_data(self):
        return {
            "fullname": self.fullname_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip(),  # có thể rỗng
            "role": 1 if self.role_combo.currentText() == "Admin" else 0
        }

    def save(self):
        if not all([
            self.fullname_input.text().strip(),
            self.phone_input.text().strip(),
            self.username_input.text().strip(),
            self.password_input.text().strip(),


        ]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        self.accept()

    def set_data(self, fullname, phone, username, role):
        self.fullname_input.setText(fullname)
        self.phone_input.setText(phone)
        self.username_input.setText(username)

        # role: 1 = Admin, 0 = Staff
        self.role_combo.setCurrentIndex(0 if role == 1 else 1)

        # Khi chỉnh sửa thì KHÔNG bắt buộc nhập mật khẩu
        self.password_input.clear()
