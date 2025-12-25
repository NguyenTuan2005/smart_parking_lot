from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QDateEdit, QPushButton
)
from PyQt6.QtCore import Qt


class ReportsTab(QWidget):
    """Tab hiển thị báo cáo chi tiết"""
    
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
        """Khởi tạo giao diện tab báo cáo"""
        layout = QVBoxLayout()

        subtitle = QLabel("📋 Báo Cáo Chi Tiết Hôm Nay")
        subtitle.setStyleSheet("font-size:16px; font-weight:bold; color:#1F618D; padding:5px;")
        layout.addWidget(subtitle)

        layout.addWidget(self._create_time_filter())

        report = QTableWidget()
        report.setColumnCount(6)
        report.setHorizontalHeaderLabels([
            "Thời Gian", "Loại Thẻ", "Biển Số", "Hành Động", "Doanh Thu", "Ghi Chú"
        ])

        data = [
            ("08:30", "Thẻ Lượt", "30-AB-123", "Vào", "50,000₫", "OK"),
            ("14:20", "Thẻ Lượt", "30-IJ-345", "Ra", "50,000₫", "OK"),
            ("10:45", "Thẻ Lượt", "30-CD-999", "Ra", "0₫", "Hết hạn"),
        ]

        report.setRowCount(len(data))
        for r, row in enumerate(data):
            for c, v in enumerate(row):
                report.setItem(r, c, QTableWidgetItem(str(v)))

        layout.addWidget(report)

        bottom = QHBoxLayout()
        today = [
            ("Xe Vào", "45", "#3498DB"),
            ("Xe Ra", "42", "#2ECC71"),
            ("Doanh Thu Hôm Nay", "850,000₫", "#E74C3C"),
            ("Trung Bình", "20,238₫/xe", "#F39C12"),
        ]
        for t, v, col in today:
            bottom.addWidget(self._create_summary_box(t, v, col))

        layout.addLayout(bottom)
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

