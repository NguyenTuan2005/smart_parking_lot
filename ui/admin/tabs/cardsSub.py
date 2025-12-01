from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from datetime import datetime


class CardSubTabLuot(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("QUẢN LÝ THẺ LƯỢT")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold; color:#2E86C1;")
        layout.addWidget(title)

        search_layout = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText("Nhập mã thẻ xe...")

        search_layout.addWidget(search_box)
        for t in ["Tìm kiếm", "Làm mới"]:
            search_layout.addWidget(QPushButton(t))
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels([
            "Mã thẻ", "Biển số", "Khách hàng", "Ngày vào",
            "Giờ vào",
            "Ngày ra",
            "Giờ ra",
            "Số ngày gửi",
            "Số lượt/Phí", "Trạng thái", "Loại thẻ","Mã nhân viên" ,"Ghi chú"
        ])

        layout.addWidget(self.table)

        data = [
            ("L001", "70-F1 666.66", "Khách vãng lai", "2025-11-01", "08:30",
             "2025-11-03", "",
             2, "0", "Đang gửi", "Thẻ lượt", "NV01", ""),
            ("L002", "30B-678.90", "Khách vãng lai","2025-11-01", "08:30",
             "2025-11-03", "09:40",
             2, "15000", "Đã ra", "Thẻ lượt","NV02", "")
        ]

        self.table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                if c == 9:
                    if "Đang gửi" in val:
                        item.setBackground(Qt.GlobalColor.red)
                        item.setForeground(Qt.GlobalColor.white)
                    else:
                        item.setBackground(Qt.GlobalColor.green)
                        item.setForeground(Qt.GlobalColor.white)
                self.table.setItem(r, c, item)

        btn_layout = QHBoxLayout()
        for t in ["Thêm thẻ mới", "Chỉnh sửa", "Xóa thẻ", "Xem chi tiết"]:
            btn_layout.addWidget(QPushButton(t))

        layout.addLayout(btn_layout)
        self.setLayout(layout)


class CardSubTabThang(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("QUẢN LÝ THẺ THÁNG")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold; color:#2E86C1;")
        layout.addWidget(title)
        search_layout = QHBoxLayout()
        search_box = QLineEdit()
        search_box.setPlaceholderText("Nhập mã thẻ xe...")

        search_layout.addWidget(search_box)
        for t in ["Tìm kiếm", "Làm mới"]:
            search_layout.addWidget(QPushButton(t))
        layout.addLayout(search_layout)
        table = QTableWidget()
        table.setColumnCount(13)
        table.setHorizontalHeaderLabels([
            "Mã thẻ", "Biển số", "Khách hàng", "Ngày vào",
            "Giờ vào",
            "Ngày ra",
            "Giờ ra",
            "Số ngày gửi",
            "Số lượt/Phí", "Trạng thái", "Loại thẻ","Mã nhân viên" ,"Ghi chú"
        ])

        data = [
            ("C101", "51C-111.22", "Lê Thị C", "2025-11-01", "08:30",
             "2025-11-03", "",
             2, "", "Đang gửi", "Thẻ tháng","NV01" ,""),
            ("C102", "49K1-999.99", "Nguyễn Minh Trí", "2025-11-01", "08:30",
             "2025-11-03", "09:40",
             2, "0", "Đã ra", "Thẻ tháng", "NV01","")
        ]

        table.setRowCount(len(data))

        for r, row in enumerate(data):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                if c == 9:
                    if "Đang gửi" in val:
                        item.setBackground(Qt.GlobalColor.red)
                        item.setForeground(Qt.GlobalColor.white)
                    else:
                        item.setBackground(Qt.GlobalColor.green)
                        item.setForeground(Qt.GlobalColor.white)
                table.setItem(r, c, item)
        layout.addWidget(table)

        btns = QHBoxLayout()
        for t in ["Thêm thẻ mới", "Chỉnh sửa", "Xóa thẻ", "Xem chi tiết"]:
            btns.addWidget(QPushButton(t))

        layout.addLayout(btns)
        self.setLayout(layout)
