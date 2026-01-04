from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton,
    QComboBox, QScrollArea
)
from PyQt6.QtCore import Qt, QDate
from controllers.StatisticsController import StatisticsController

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    FigureCanvas = None
    Figure = None

try:
    import seaborn as sns

    HAS_SEABORN = True
    sns.set_theme(style="whitegrid")
except ImportError:
    HAS_SEABORN = False
    sns = None


class ChartsTab(QWidget):
    """Tab hiển thị các biểu đồ thống kê"""

    def __init__(self):
        super().__init__()
        if not HAS_MATPLOTLIB:
            layout = QVBoxLayout()
            msg = QLabel("Cần cài đặt matplotlib để xem biểu đồ:\npip install matplotlib seaborn")
            msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            msg.setStyleSheet("font-size:14px; color:#E74C3C; padding:20px;")
            layout.addWidget(msg)
            self.setLayout(layout)
            return

        self.controller = StatisticsController(self)
        self.start_date = None
        self.end_date = None

        self.initUI()

    def _create_time_filter(self):
        """Tạo bộ lọc thời gian dùng chung"""
        filter_widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(12)

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("dd/MM/yyyy")
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("dd/MM/yyyy")
        self.end_date_edit.setDate(QDate.currentDate())

        layout.addWidget(QLabel("Từ ngày:"))
        layout.addWidget(self.start_date_edit)
        layout.addWidget(QLabel("Đến ngày:"))
        layout.addWidget(self.end_date_edit)

        quick = ["Hôm nay", "Tuần này", "Tháng này", "Năm nay"]
        for q in quick:
            b = QPushButton(q)
            b.setStyleSheet("""
                QPushButton {
                    padding: 5px 10px;
                    background: #3498DB;
                    color: white;
                    border-radius: 5px;
                    border: 1px solid #2980B9;
                }
                QPushButton:hover {
                    background: #2980B9;
                    border: 1px solid #21618C;
                }
                QPushButton:pressed {
                    background: #21618C;
                    border: 1px solid #1B4F72;
                }
            """)
            b.clicked.connect(lambda checked, name=q: self._on_quick_filter_clicked(name))
            layout.addWidget(b)

        btn_apply = QPushButton("Áp dụng")
        btn_apply.setStyleSheet("""
            QPushButton {
                padding: 6px 14px;
                background: #27AE60;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                border: 1px solid #229954;
            }
            QPushButton:hover {
                background: #229954;
                border: 1px solid #1E8449;
            }
            QPushButton:pressed {
                background: #1E8449;
                border: 1px solid #145A32;
            }
        """)
        btn_apply.clicked.connect(self._on_apply_filter)
        layout.addWidget(btn_apply)

        filter_widget.setLayout(layout)
        return filter_widget

    def _on_quick_filter_clicked(self, filter_name: str):
        """Xử lý khi click nút filter nhanh"""
        start_date, end_date = self.controller.get_date_range_from_quick_filter(filter_name)

        self.start_date_edit.setDate(QDate.fromString(
            start_date.strftime("%d/%m/%Y"), "dd/MM/yyyy"
        ))
        self.end_date_edit.setDate(QDate.fromString(
            end_date.strftime("%d/%m/%Y"), "dd/MM/yyyy"
        ))

        self._apply_date_filter(start_date, end_date)

    def _on_apply_filter(self):
        """Xử lý khi click nút Áp dụng"""
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()

        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        self._apply_date_filter(start_datetime, end_datetime)

    def _apply_date_filter(self, start_date: datetime, end_date: datetime):
        """Áp dụng filter và cập nhật biểu đồ"""
        self.start_date = start_date
        self.end_date = end_date

        current_key = self.chart_selector.currentData()
        if current_key:
            self._update_chart_canvas(current_key)

    def initUI(self):
        """Khởi tạo giao diện tab biểu đồ"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 10, 20, 20)
        layout.setSpacing(12)

        subtitle = QLabel("📈 Biểu Đồ Thống Kê")
        subtitle.setStyleSheet("font-size:16px; font-weight:bold; color:#1F618D; padding:5px;")
        layout.addWidget(subtitle)

        layout.addWidget(self._create_time_filter())

        selector_row = QHBoxLayout()
        selector_row.setSpacing(10)
        selector_label = QLabel("Chọn biểu đồ:")
        selector_label.setStyleSheet("font-weight:bold;")
        selector_row.addWidget(selector_label)

        self.chart_selector = QComboBox()
        for key, label in self._chart_options():
            self.chart_selector.addItem(label, key)
        self.chart_selector.currentIndexChanged.connect(self._on_chart_changed)
        selector_row.addWidget(self.chart_selector)
        selector_row.addStretch()

        layout.addLayout(selector_row)

        self.chart_hint_label = QLabel("")
        self.chart_hint_label.setStyleSheet("color:#BDC3C7; font-size:11px; margin-bottom:4px;")
        layout.addWidget(self.chart_hint_label)

        # Thêm scroll area để đảm bảo hiển thị đầy đủ
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.chart_container = QWidget()
        self.chart_container_layout = QVBoxLayout()
        self.chart_container_layout.setContentsMargins(5, 5, 5, 5)
        self.chart_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.chart_container.setLayout(self.chart_container_layout)

        scroll_area.setWidget(self.chart_container)
        layout.addWidget(scroll_area)

        self._update_chart_canvas(self.chart_selector.currentData())

        self.setLayout(layout)

    def _chart_options(self):
        """Danh sách các loại biểu đồ"""
        return [
            ("revenue", "Doanh thu theo tháng"),
            ("traffic", "Lượt xe theo giờ & ngày"),
            ("dow_entries", "Lượt vào/ra theo ngày trong tuần"),
            ("hour_hist", "Phân bố lượt xe theo giờ"),
        ]

    def _chart_descriptions(self):
        """Mô tả các loại biểu đồ"""
        return {
            "revenue": "Theo dõi xu hướng doanh thu các tháng để đánh giá tăng trưởng.",
            "traffic": "Nhận diện khung giờ và ngày cao điểm để bố trí nhân sự.",
            "dow_entries": "So sánh lượt vào/ra theo ngày để thấy ngày cao điểm.",
            "hour_hist": "Phân bố lượt xe theo giờ để chọn khung mở rộng/thu hẹp ca.",
        }

    def _on_chart_changed(self, index):
        """Xử lý khi người dùng chọn biểu đồ khác"""
        key = self.chart_selector.itemData(index)
        self._update_chart_canvas(key)

    def _update_chart_canvas(self, key):
        """Cập nhật biểu đồ theo key được chọn"""
        while self.chart_container_layout.count():
            item = self.chart_container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        chart_widget = None
        if key == "revenue":
            chart_widget = self._chart_revenue_trend()
        # elif key == "mix":
        #     chart_widget = self._chart_vehicle_mix()
        # elif key == "duration":
        #     chart_widget = self._chart_duration_boxplot()
        elif key == "traffic":
            chart_widget = self._chart_traffic_heatmap()
        elif key == "dow_entries":
            chart_widget = self._chart_dow_entries()
        # elif key == "fee_duration":
        #     chart_widget = self._chart_fee_vs_duration()
        elif key == "hour_hist":
            chart_widget = self._chart_hour_hist()

        desc = self._chart_descriptions().get(key, "")
        self.chart_hint_label.setText(desc)

        if chart_widget:
            self.chart_container_layout.addWidget(chart_widget)

    def _create_figure(self, figsize=(12, 9)):
        """Tạo figure với padding đủ lớn"""
        figure = Figure(figsize=figsize, dpi=100)
        # Tăng padding top để tránh cắt tiêu đề
        figure.subplots_adjust(left=0.1, right=0.95, top=0.90, bottom=0.12)
        return figure

    def _chart_revenue_trend(self):
        figure = self._create_figure()
        ax = figure.add_subplot(111)

        months, revenues = self.controller.get_revenue_trend_data(
            start_date=self.start_date, end_date=self.end_date
        )

        if HAS_SEABORN:
            sns.lineplot(x=months, y=revenues, marker="o", ax=ax, color="#2E86C1", linewidth=2.5)
        else:
            ax.plot(months, revenues, marker="o", color="#2E86C1", linewidth=2.5)

        # Thêm chú thích giá trị tại mỗi điểm
        for i, (month, revenue) in enumerate(zip(months, revenues)):
            ax.annotate(f'{revenue:.1f}', 
                       xy=(month, revenue), 
                       xytext=(5, 5), 
                       textcoords='offset points',
                       fontsize=9, 
                       color='#2E86C1',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        # Thêm thông tin tổng quan
        total_revenue = sum(revenues)
        ax.text(0.02, 0.98, f'Tổng doanh thu: {total_revenue:.1f} triệu đồng', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.set_title("Doanh Thu Theo Tháng", fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel("Triệu đồng", fontsize=11)
        ax.set_xlabel("Tháng", fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.tick_params(axis='x', rotation=45)

        return FigureCanvas(figure)

    def _chart_vehicle_mix(self):
        figure = self._create_figure()
        ax = figure.add_subplot(111)

        labels, values = self.controller.get_vehicle_mix_data(self.start_date, self.end_date)

        if HAS_SEABORN:
            sns.barplot(x=labels, y=values,hue=labels, ax=ax, palette="Blues", legend=False)
        else:
            ax.bar(labels, values, color="#3498DB")

        ax.set_title("Cơ Cấu Lượt Xe", fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel("Số lượt", fontsize=11)
        ax.set_xlabel("Nhóm khách", fontsize=11)
        ax.tick_params(axis="x", rotation=0)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')

        return FigureCanvas(figure)

    def _chart_duration_boxplot(self):
        figure = self._create_figure()
        ax = figure.add_subplot(111)

        samples = self.controller.get_duration_boxplot_data(self.start_date, self.end_date)

        labels = []
        durations = []
        for k, vals in samples.items():
            labels.extend([k] * len(vals))
            durations.extend(vals)

        if HAS_SEABORN:
            sns.boxplot(x=labels, y=durations, ax=ax, hue=labels, palette="Set2", legend=False)
        else:
            ax.scatter(labels, durations, alpha=0.6, color="#2ECC71")

        ax.set_title("Thời Gian Đỗ Xe Theo Nhóm", fontsize=14, fontweight='bold', pad=20)
        ax.set_ylabel("Phút đỗ", fontsize=11)
        ax.set_xlabel("Nhóm khách", fontsize=11)
        ax.tick_params(axis="x", rotation=0)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')

        return FigureCanvas(figure)

    def _chart_traffic_heatmap(self):
        figure = self._create_figure(figsize=(13, 7))
        ax = figure.add_subplot(111)

        days, hours, traffic = self.controller.get_traffic_heatmap_data(
            self.start_date, self.end_date
        )

        if HAS_SEABORN:
            sns.heatmap(
                traffic,
                annot=True,
                fmt="d",
                cmap="YlOrRd",
                xticklabels=hours,
                yticklabels=days,
                ax=ax,
                cbar_kws={'label': 'Số lượt xe'}
            )
            ax.set_xlabel("Khung giờ", fontsize=11)
            ax.set_ylabel("Ngày", fontsize=11)
            ax.set_title("Mật Độ Lượt Xe Theo Giờ & Ngày", fontsize=14, fontweight='bold', pad=15)
        else:
            ax.set_title("Cần cài seaborn để xem heatmap", fontsize=14)
            ax.axis("off")

        return FigureCanvas(figure)

    def _chart_dow_entries(self):
        figure = self._create_figure()
        ax = figure.add_subplot(111)

        days, entries, exits = self.controller.get_dow_entries_data(
            self.start_date, self.end_date
        )

        x = range(len(days))
        width = 0.35

        bars1 = ax.bar([i - width / 2 for i in x], entries, width, label='Vào', color='#3498DB', alpha=0.9)
        bars2 = ax.bar([i + width / 2 for i in x], exits, width, label='Ra', color='#2ECC71', alpha=0.9)

        # Thêm chú thích giá trị trên mỗi bar
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9, color='#3498DB')

        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9, color='#2ECC71')

        ax.set_title("Lượt Vào/Ra Theo Ngày", fontsize=14, fontweight='bold', pad=15)
        ax.set_ylabel("Số lượt", fontsize=11)
        ax.set_xlabel("Ngày", fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(days)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')

        return FigureCanvas(figure)

    def _chart_fee_vs_duration(self):
        figure = self._create_figure()
        ax = figure.add_subplot(111)

        duration, fee = self.controller.get_fee_vs_duration_data(
            self.start_date, self.end_date
        )

        if HAS_SEABORN:
            sns.regplot(
                x=duration, y=fee, ax=ax,
                scatter_kws={"alpha": 0.5, "s": 30},
                line_kws={"color": "#E74C3C", "linewidth": 2}
            )
        else:
            ax.scatter(duration, fee, alpha=0.5, color="#2980B9", s=30)
            if duration:
                m, b = 0.4, 7
                xs = [min(duration), max(duration)]
                ys = [m * x + b for x in xs]
                ax.plot(xs, ys, color="#E74C3C", linewidth=2)

        ax.set_title("Tương Quan Phí vs Thời Gian Đỗ", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel("Phút đỗ", fontsize=11)
        ax.set_ylabel("Phí (nghìn đồng)", fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')

        return FigureCanvas(figure)

    def _chart_hour_hist(self):
        figure = self._create_figure()
        ax = figure.add_subplot(111)

        hour_data = self.controller.get_hour_histogram_data(
            self.start_date, self.end_date
        )

        hours = []
        for hour in range(24):
            hours.extend([hour] * hour_data[hour])

        if HAS_SEABORN:
            sns.histplot(hours, bins=24, ax=ax, color="#9B59B6", kde=True, line_kws={"linewidth": 2})
        else:
            ax.hist(hours, bins=24, color="#9B59B6", alpha=0.85)

        # Thêm chú thích giá trị trên mỗi bar
        for i, count in enumerate(hour_data):
            if count > 0:
                ax.text(i, count + 0.5, f'{count}', ha='center', va='bottom', fontsize=8, color='#9B59B6')

        ax.set_title("Phân Bố Lượt Xe Theo Giờ", fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel("Giờ trong ngày", fontsize=11)
        ax.set_ylabel("Số lượt", fontsize=11)
        ax.set_xticks(range(0, 24, 2))
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')

        return FigureCanvas(figure)