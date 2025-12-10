from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt


class VehicleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # =========================
        #        TIÊU ĐỀ
        # =========================
        title = QLabel("QUẢN LÝ PHƯƠNG TIỆN")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:#2E86C1;
        """)
        layout.addWidget(title)

        # =========================
        #      THANH TÌM KIẾM
        # =========================
        search = QHBoxLayout()

        box = QLineEdit()
        box.setPlaceholderText("Nhập biển số phương tiện...")
        box.setStyleSheet("padding: 6px; font-size: 14px;")
        search.addWidget(box)

        for t in ["Tìm kiếm", "Làm mới"]:
            btn = QPushButton(t)
            btn.setStyleSheet("padding: 6px 12px; font-size: 14px;")
            search.addWidget(btn)

        layout.addLayout(search)

        # =========================
        #       BẢNG DỮ LIỆU
        # =========================
        table = QTableWidget()
        table.setColumnCount(3)

        table.setHorizontalHeaderLabels([
            "Tên khách hàng",
            "Biển số",
            "Loại phương tiện",
            "Ghi chú"
        ])

        # Căn cột tự giãn
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(table)

        # =========================
        #       DỮ LIỆU MẪU
        # =========================
        data = [
            ("Nguyen Văn Hồ","70-F1 666.66", "Xe máy",
              ""),

            ("Hồ Văn Bao","30B-678.90", "Xe máy", "")
        ]

        table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(str(val)))

        # =========================
        #      NÚT CHỨC NĂNG
        # =========================
        btns = QHBoxLayout()
        btns.setSpacing(10)

        for t in ["Thêm phương tiện", "Chỉnh sửa", "Xóa phương tiện", "Xem chi tiết"]:
            b = QPushButton(t)
            b.setStyleSheet("""
                padding: 8px 14px;
                background-color: #3498DB;
                color: white;
                border-radius: 4px;
                font-size: 14px;
            """)
            btns.addWidget(b)

        layout.addLayout(btns)

        self.setLayout(layout)
