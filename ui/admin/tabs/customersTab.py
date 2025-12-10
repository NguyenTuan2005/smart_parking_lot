from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt
from ui.common.renewalDialog import RenewalDialog
from datetime import datetime


class CustomerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Layout chính
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # ================================
        #  TIÊU ĐỀ
        # ================================
        title = QLabel("QUẢN LÝ KHÁCH HÀNG")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2E86C1;
        """)
        layout.addWidget(title)

        # ================================
        #  Ô TÌM KIẾM
        # ================================
        search_layout = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText("Nhập tên khách hàng...")
        search_box.setStyleSheet("padding: 6px; font-size: 14px;")

        btn_search = QPushButton("Tìm kiếm")
        btn_refresh = QPushButton("Làm mới")

        for btn in (btn_search, btn_refresh):
            btn.setStyleSheet("padding: 6px 12px; font-size: 14px;")

        search_layout.addWidget(search_box)
        search_layout.addWidget(btn_search)
        search_layout.addWidget(btn_refresh)
        layout.addLayout(search_layout)

        # ================================
        #  BẢNG DANH SÁCH KHÁCH HÀNG
        # ================================
        self.table = QTableWidget()
        # add one more column for Active status
        self.table.setColumnCount(12)

        self.table.setHorizontalHeaderLabels([
            "Mã KH",
            "Mã thẻ",
            "Biển số đăng ký",
            "Tên khách hàng",
            "Ngày bắt đầu",
            "Ngày hết hạn",
            "Số ngày còn lại",
            "Số điện thoại",
            "Email",
            "Giá vé",
            "Ghi chú",
            "Còn hoạt động"
        ])

        # Căn chỉnh cột tự giãn
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

        # ================================
        #  DỮ LIỆU MẪU
        # ================================
        data = [
            ("KH001", "C101","70H1-25678" ,"Nguyễn Minh Trí", "2025-01-01", "2025-06-01", "120", "0987654321","example@gmail.com","150000", ""),
            ("KH002", "C102","70H1-25678", "Trần Văn B",   "2025-02-10", "2025-07-10", "150", "0912345678","example@gmail.com","150000", "")
        ]

        self.table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))
            # placeholder for Active column (last column)
            self.table.setItem(r, 11, QTableWidgetItem(""))

        # Note: status calculation and notification logic are intentionally
        # not implemented here — this tab only provides the columns/UI.

        # ================================
        #  NÚT CHỨC NĂNG
        # ================================
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        buttons = ["Thêm KH", "Chỉnh sửa", "Xóa KH", "Xem chi tiết"]
        for text in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                padding: 8px 14px;
                background-color: #3498DB;
                color: white;
                border-radius: 4px;
                font-size: 14px;
            """)
            button_layout.addWidget(btn)

        # Notification button for expired customers
        notify_btn = QPushButton("Gửi thông báo gia hạn")
        notify_btn.setStyleSheet("padding: 8px 14px; background-color: #E67E22; color: white; border-radius:4px; font-size:14px;")
        # Open renewal dialog when clicked
        notify_btn.clicked.connect(self._open_renewal_dialog)
        button_layout.addWidget(notify_btn)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _open_renewal_dialog(self):
        """Open renewal dialog. If a single row is selected, prefill email and suggested fee."""
        selected = self.table.selectionModel().selectedRows()
        email = ""
        suggested_fee = None
        current_end = None
        if selected and len(selected) == 1:
            r = selected[0].row()
            # Email is column 8
            email_item = self.table.item(r, 8)
            if email_item:
                email = email_item.text()
            # Fee is column 9
            fee_item = self.table.item(r, 9)
            if fee_item:
                try:
                    suggested_fee = int(str(fee_item.text()).replace(",", ""))
                except Exception:
                    suggested_fee = None
            # current end date is column 5
            end_item = self.table.item(r, 5)
            if end_item:
                current_end = end_item.text()

        dlg = RenewalDialog(self, email=email, current_end=current_end, suggested_fee=suggested_fee)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            # Optionally update note column to reflect that a notice was 'sent'
            if selected and len(selected) == 1:
                r = selected[0].row()
                note_item = self.table.item(r, 10)
                if not note_item:
                    note_item = QTableWidgetItem("")
                    self.table.setItem(r, 10, note_item)
                note_item.setText("Đã gửi thông báo gia hạn (UI)")
