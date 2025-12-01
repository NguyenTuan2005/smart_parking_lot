from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt


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
        self.table.setColumnCount(10)

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
            "Ghi chú"
        ])

        # Căn chỉnh cột tự giãn
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

        # ================================
        #  DỮ LIỆU MẪU
        # ================================
        data = [
            ("KH001", "C101","70H1-25678" ,"Nguyễn Minh Trí", "2025-01-01", "2025-06-01", "120", "0987654321","example@gmail.com", ""),
            ("KH002", "C102","70H1-25678", "Trần Văn B",   "2025-02-10", "2025-07-10", "150", "0912345678","example@gmail.com", "")
        ]

        self.table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                self.table.setItem(r, c, QTableWidgetItem(str(val)))

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

        layout.addLayout(button_layout)

        self.setLayout(layout)
