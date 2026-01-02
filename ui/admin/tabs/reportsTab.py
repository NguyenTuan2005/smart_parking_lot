from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem,
    QDateEdit, QPushButton, QHeaderView
)
from PyQt6.QtCore import Qt, QDate


class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def _create_time_filter(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setSpacing(12)

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("dd/MM/yyyy")
        self.start_date_input.setDate(QDate.currentDate())

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDisplayFormat("dd/MM/yyyy")
        self.end_date_input.setDate(QDate.currentDate())

        self.btn_today = QPushButton("Hôm nay")
        self.btn_apply = QPushButton("🔍 Áp dụng")

        layout.addWidget(QLabel("Từ ngày:"))
        layout.addWidget(self.start_date_input)
        layout.addWidget(QLabel("Đến ngày:"))
        layout.addWidget(self.end_date_input)
        layout.addWidget(self.btn_today)
        layout.addWidget(self.btn_apply)
        layout.addStretch()

        return widget

    def initUI(self):
        layout = QVBoxLayout(self)

        title = QLabel("📋 BÁO CÁO HOẠT ĐỘNG VÀ DOANH THU")
        title.setStyleSheet("font-size:18px;font-weight:bold;color:#1F618D")
        layout.addWidget(title)

        layout.addWidget(self._create_time_filter())

        self.report_table = QTableWidget()
        self.report_table.setColumnCount(6)
        self.report_table.setHorizontalHeaderLabels([
            "Thời Gian", "Loại Thẻ", "Biển Số",
            "Hành Động", "Doanh Thu", "Ghi Chú"
        ])

        self.report_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.report_table.verticalHeader().setVisible(False)

        layout.addWidget(self.report_table)

        bottom = QHBoxLayout()
        self.box_in, self.lbl_in = self._box("Xe Vào", "0", "#3498DB")
        self.box_out, self.lbl_out = self._box("Xe Ra", "0", "#2ECC71")
        self.box_rev, self.lbl_rev = self._box("Doanh Thu", "0₫", "#E74C3C")
        self.box_avg, self.lbl_avg = self._box("Trung Bình", "0₫/xe", "#F39C12")

        for b in [self.box_in, self.box_out, self.box_rev, self.box_avg]:
            bottom.addWidget(b)

        layout.addLayout(bottom)

    def _box(self, title, value, color):
        box = QWidget()
        v = QVBoxLayout(box)
        v.addWidget(QLabel(f"<b>{title}</b>"))

        lbl = QLabel(value)
        lbl.setStyleSheet(f"font-size:20px;color:{color};font-weight:bold")
        v.addWidget(lbl)

        box.setStyleSheet(f"""
            QWidget {{
                border:2px solid {color};
                border-radius:10px;
                padding:10px;
            }}
        """)
        return box, lbl

    def update_ui(self, data):
        self.report_table.setRowCount(0)

        for r, row in enumerate(data["table_data"]):
            self.report_table.insertRow(r)
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.report_table.setItem(r, c, item)

        self.lbl_in.setText(data["stats"]["in"])
        self.lbl_out.setText(data["stats"]["out"])
        self.lbl_rev.setText(data["stats"]["revenue"])
        self.lbl_avg.setText(data["stats"]["avg"])
