from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QDateEdit, QPushButton
)
from PyQt6.QtCore import Qt


class OverviewTab(QWidget):
    """Tab hiển thị tổng quan thống kê bãi xe"""
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def _create_time_filter(self):
        """Tạo bộ lọc thời gian dùng chung"""
        filter_widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(12)

        # Từ ngày
        start_date = QDateEdit()
        start_date.setCalendarPopup(True)
        start_date.setDisplayFormat("dd/MM/yyyy")

        # Đến ngày
        end_date = QDateEdit()
        end_date.setCalendarPopup(True)
        end_date.setDisplayFormat("dd/MM/yyyy")

        layout.addWidget(QLabel("Từ ngày:"))
        layout.addWidget(start_date)

        layout.addWidget(QLabel("Đến ngày:"))
        layout.addWidget(end_date)

        # Nút lọc nhanh
        quick = ["Hôm nay", "Tuần này", "Tháng này", "Năm nay"]
        for q in quick:
            b = QPushButton(q)
            b.setStyleSheet("""
                padding: 5px 10px;
                background:#3498DB;
                color:white;
                border-radius:5px;
            """)
            layout.addWidget(b)

        # Nút áp dụng
        btn_apply = QPushButton("Áp dụng")
        btn_apply.setStyleSheet("""
            padding:6px 14px;
            background:#27AE60;
            color:white;
            font-weight:bold;
            border-radius:5px;
        """)
        layout.addWidget(btn_apply)

        filter_widget.setLayout(layout)
        return filter_widget

    def initUI(self):
        """Khởi tạo giao diện tab tổng quan"""
        layout = QVBoxLayout()

        subtitle = QLabel("📊 Tổng Quan Bãi Xe")
        subtitle.setStyleSheet("font-size:16px; font-weight:bold; color:#1F618D; padding:5px;")
        layout.addWidget(subtitle)

        layout.addWidget(self._create_time_filter())

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels([
            "Loại Thẻ", "Số Lượng Thẻ", "Số Xe Hiện Tại", "Doanh Thu", "Tỷ Lệ %"
        ])

        data = [
            ("Thẻ Lượt", 20, 15, "5,000,000₫", "45%"),
            ("Thẻ Tháng", 10, 8, "12,000,000₫", "55%")
        ]

        table.setRowCount(len(data))
        for r, row in enumerate(data):
            for c, v in enumerate(row):
                table.setItem(r, c, QTableWidgetItem(str(v)))
        layout.addWidget(table)

        summary = QHBoxLayout()
        info = [
            ("Tổng Doanh Thu", "17,000,000₫", "#27AE60"),
            ("Tổng Xe", "23", "#3498DB"),
            ("Tổng Thẻ", "30", "#E74C3C"),
            ("Lượt Ra Vào", "145", "#F39C12"),
        ]
        for t, v, col in info:
            summary.addWidget(self._create_summary_box(t, v, col))

        layout.addLayout(summary)
        self.setLayout(layout)

    def _create_summary_box(self, title, value, color):
        """Tạo box tóm tắt nhanh"""
        box = QWidget()
        v = QVBoxLayout()
        v.addWidget(QLabel(f"<b>{title}</b>"))
        lbl = QLabel(value)
        lbl.setStyleSheet(f"font-size:18px; color:{color}; font-weight:bold;")
        v.addWidget(lbl)
        box.setLayout(v)
        box.setStyleSheet(f"""
                    QWidget {{
                        border:2px solid {color};
                        border-radius:10px;
                        background:#F8F9F9;
                        padding:10px;
                    }}
                """)
        return box

