from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QTabWidget, QDateEdit, QPushButton
)
from PyQt6.QtCore import Qt, QDate

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    FigureCanvas = None
    Figure = None


class StatsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # ============================================
    #   TẠO BỘ LỌC THỜI GIAN DÙNG CHUNG
    # ============================================
    def _create_time_filter(self):
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

    # ============================================
    #   KHỞI TẠO GIAO DIỆN CHÍNH
    # ============================================
    def initUI(self):
        main_layout = QVBoxLayout()

        title = QLabel("THỐNG KÊ VÀ BÁO CÁO BÃI XE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold; color:#2E86C1; padding:10px;")
        main_layout.addWidget(title)

        stats_tabs = QTabWidget()

        stats_tabs.addTab(self._create_overview_tab(), "Tổng Quan")

        if HAS_MATPLOTLIB:
            stats_tabs.addTab(self._create_charts_tab(), "Biểu Đồ")

        stats_tabs.addTab(self._create_report_tab(), "Báo Cáo Chi Tiết")

        main_layout.addWidget(stats_tabs)
        self.setLayout(main_layout)

    # ============================================
    #       TAB TỔNG QUAN
    # ============================================
    def _create_overview_tab(self):
        widget = QWidget()
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
        widget.setLayout(layout)
        return widget

    # Box tóm tắt nhanh
    def _create_summary_box(self, title, value, color):
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

    # ============================================
    #       TAB BÁO CÁO CHI TIẾT
    # ============================================
    def _create_report_tab(self):
        widget = QWidget()
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
        widget.setLayout(layout)
        return widget

    # ============================================
    #       TAB BIỂU ĐỒ
    # ============================================
    def _create_charts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        subtitle = QLabel("📈 Biểu Đồ Thống Kê")
        subtitle.setStyleSheet("font-size:16px; font-weight:bold; color:#1F618D; padding:5px;")
        layout.addWidget(subtitle)

        layout.addWidget(self._create_time_filter())

        charts = QHBoxLayout()
        charts.addWidget(self._chart_revenue())
        charts.addWidget(self._chart_distribution())

        layout.addLayout(charts)
        widget.setLayout(layout)
        return widget

    # Biểu đồ doanh thu
    def _chart_revenue(self):
        figure = Figure(figsize=(4, 3))
        ax = figure.add_subplot(111)

        months = ["T1", "T2", "T3", "T4", "T5"]
        revenue = [10, 12, 8, 15, 17]

        ax.bar(months, revenue)
        ax.set_title("Doanh Thu Tháng")
        ax.set_ylabel("Triệu đồng")

        return FigureCanvas(figure)

    # Biểu đồ phân bố
    def _chart_distribution(self):
        figure = Figure(figsize=(4, 3))
        ax = figure.add_subplot(111)

        labels = ["Thẻ Lượt", "Thẻ Tháng", "Khách"]
        values = [35, 45, 20]

        ax.pie(values, labels=labels, autopct="%1.1f%%")
        ax.set_title("Phân Bố Xe")

        return FigureCanvas(figure)
