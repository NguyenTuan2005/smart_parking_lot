from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QMessageBox, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime, timedelta


class RenewalDialog(QDialog):


    def __init__(self, parent=None, email: str = "", current_end: str | None = None, suggested_fee: int | None = None):
        super().__init__(parent)
        self.setWindowTitle("Gửi thông báo gia hạn")
        self.setModal(True)
        self.resize(420, 260)

        layout = QVBoxLayout()

        # Email
        layout.addWidget(QLabel("Email khách hàng:"))
        self.email_input = QLineEdit()
        self.email_input.setText(email)
        layout.addWidget(self.email_input)

        # Renewal end date
        layout.addWidget(QLabel("Thời gian gia hạn (ngày hết hạn mới):"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        # default: if current_end provided, add 30 days; else today +30
        try:
            if current_end:
                dt = datetime.strptime(current_end, "%Y-%m-%d")
            else:
                dt = datetime.now()
        except Exception:
            dt = datetime.now()
        default_new = dt + timedelta(days=30)
        self.date_edit.setDate(QDate(default_new.year, default_new.month, default_new.day))
        layout.addWidget(self.date_edit)

        # Renewal fee
        layout.addWidget(QLabel("Phí gia hạn (VND):"))
        self.fee_input = QLineEdit()
        if suggested_fee is not None:
            self.fee_input.setText(str(suggested_fee))
        layout.addWidget(self.fee_input)

        # Bank transfer info (read-only)
        layout.addWidget(QLabel("Thông tin chuyển khoản:"))
        bank_info = QLabel("Ngân hàng ABC - STK: 0123456789 - Chủ TK: Công ty XYZ")
        bank_info.setWordWrap(True)
        bank_info.setStyleSheet("background-color: #000; padding:6px; border-radius:4px;")
        layout.addWidget(bank_info)

        # Buttons
        btn_layout = QHBoxLayout()
        self.send_btn = QPushButton("Gửi")
        self.send_btn.clicked.connect(self._on_send)
        btn_layout.addWidget(self.send_btn)

        self.cancel_btn = QPushButton("Hủy")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def _on_send(self):
        email = self.email_input.text().strip()
        fee_text = self.fee_input.text().replace(",", "").strip()
        if not email:
            QMessageBox.critical(self, "Lỗi", "Vui lòng nhập email khách hàng.")
            return
        try:
            fee = int(fee_text)
            if fee < 0:
                raise ValueError()
        except Exception:
            QMessageBox.critical(self, "Lỗi", "Vui lòng nhập Phí gia hạn hợp lệ (số nguyên).")
            return

        # UI-only: simulate sending
        QMessageBox.information(self, "Gửi thông báo", f"Đã gửi thông báo đến {email}.\nPhí gia hạn: {fee} VND")
        self.accept()
