from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QPushButton,
    QComboBox
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
            # Nếu không có matplotlib, hiển thị thông báo
            layout = QVBoxLayout()
            msg = QLabel("Cần cài đặt matplotlib để xem biểu đồ:\npip install matplotlib seaborn")
            msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
            msg.setStyleSheet("font-size:14px; color:#E74C3C; padding:20px;")
            layout.addWidget(msg)
            self.setLayout(layout)
            return
        
        # Import controller sau khi đảm bảo có matplotlib
        from controllers.StatisticsController import StatisticsController
        self.controller = StatisticsController(self)
        
        # Biến lưu filter
        self.start_date = None
        self.end_date = None
        
        self.initUI()

    def _create_time_filter(self):
        """Tạo bộ lọc thời gian dùng chung"""
        filter_widget = QWidget()
        layout = QHBoxLayout()
        layout.setSpacing(12)

        # Từ ngày
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat("dd/MM/yyyy")
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))  # Mặc định 30 ngày trước

        # Đến ngày
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("dd/MM/yyyy")
        self.end_date_edit.setDate(QDate.currentDate())  # Mặc định hôm nay

        layout.addWidget(QLabel("Từ ngày:"))
        layout.addWidget(self.start_date_edit)

        layout.addWidget(QLabel("Đến ngày:"))
        layout.addWidget(self.end_date_edit)

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
            b.clicked.connect(lambda checked, name=q: self._on_quick_filter_clicked(name))
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
        btn_apply.clicked.connect(self._on_apply_filter)
        layout.addWidget(btn_apply)

        filter_widget.setLayout(layout)
        return filter_widget

    def _on_quick_filter_clicked(self, filter_name: str):
        """Xử lý khi click nút filter nhanh"""
        start_date, end_date = self.controller.get_date_range_from_quick_filter(filter_name)
        
        # Cập nhật date edit
        self.start_date_edit.setDate(QDate.fromString(
            start_date.strftime("%d/%m/%Y"), "dd/MM/yyyy"
        ))
        self.end_date_edit.setDate(QDate.fromString(
            end_date.strftime("%d/%m/%Y"), "dd/MM/yyyy"
        ))
        
        # Áp dụng filter
        self._apply_date_filter(start_date, end_date)

    def _on_apply_filter(self):
        """Xử lý khi click nút Áp dụng"""
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()
        
        # Chuyển sang datetime với thời gian đầy đủ
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())
        
        self._apply_date_filter(start_datetime, end_datetime)

    def _apply_date_filter(self, start_date: datetime, end_date: datetime):
        """Áp dụng filter và cập nhật biểu đồ"""
        self.start_date = start_date
        self.end_date = end_date
        
        # Cập nhật lại biểu đồ hiện tại
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

        # Thanh chọn loại biểu đồ để tiết kiệm không gian
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

        # Gợi ý ngắn về ý nghĩa biểu đồ
        self.chart_hint_label = QLabel("")
        self.chart_hint_label.setStyleSheet("color:#BDC3C7; font-size:11px; margin-bottom:4px;")
        layout.addWidget(self.chart_hint_label)

        # Khu vực hiển thị biểu đồ thay đổi theo menu
        self.chart_container = QWidget()
        self.chart_container_layout = QVBoxLayout()
        self.chart_container_layout.setContentsMargins(10, 0, 10, 0)
        self.chart_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_container.setLayout(self.chart_container_layout)
        self.chart_container.setMinimumHeight(420)  # khung cao hơn để nhìn rõ biểu đồ
        layout.addWidget(self.chart_container)

        # Render biểu đồ mặc định
        self._update_chart_canvas(self.chart_selector.currentData())

        self.setLayout(layout)

    def _chart_options(self):
        """Danh sách các loại biểu đồ"""
        return [
            ("revenue", "Doanh thu theo tháng"),
            ("mix", "Cơ cấu lượt xe (gộp thẻ lượt & khách vãng lai)"),
            ("duration", "Thời gian đỗ xe theo nhóm khách"),
            ("traffic", "Lượt xe theo giờ & ngày"),
            ("dow_entries", "Lượt vào/ra theo ngày trong tuần"),
            ("fee_duration", "Tương quan phí & thời gian đỗ"),
            ("hour_hist", "Phân bố lượt xe theo giờ"),
        ]

    def _chart_descriptions(self):
        """Mô tả các loại biểu đồ"""
        return {
            "revenue": "Theo dõi xu hướng doanh thu các tháng để đánh giá tăng trưởng.",
            "mix": "So sánh tỷ trọng khách dùng thẻ tháng và khách đi lượt/vãng lai.",
            "duration": "Nhìn nhanh phân bố thời gian đỗ của từng nhóm khách.",
            "traffic": "Nhận diện khung giờ và ngày cao điểm để bố trí nhân sự.",
            "dow_entries": "So sánh lượt vào/ra theo ngày để thấy ngày cao điểm.",
            "fee_duration": "Kiểm tra phí thu có tỷ lệ thuận thời gian đỗ hay không.",
            "hour_hist": "Phân bố lượt xe theo giờ để chọn khung mở rộng/thu hẹp ca.",
        }

    def _on_chart_changed(self, index):
        """Xử lý khi người dùng chọn biểu đồ khác"""
        key = self.chart_selector.itemData(index)
        self._update_chart_canvas(key)

    def _update_chart_canvas(self, key):
        """Cập nhật biểu đồ theo key được chọn"""
        # Xóa biểu đồ cũ
        while self.chart_container_layout.count():
            item = self.chart_container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        chart_widget = None
        if key == "revenue":
            chart_widget = self._chart_revenue_trend()
        elif key == "mix":
            chart_widget = self._chart_vehicle_mix()
        elif key == "duration":
            chart_widget = self._chart_duration_boxplot()
        elif key == "traffic":
            chart_widget = self._chart_traffic_heatmap()
        elif key == "dow_entries":
            chart_widget = self._chart_dow_entries()
        elif key == "fee_duration":
            chart_widget = self._chart_fee_vs_duration()
        elif key == "hour_hist":
            chart_widget = self._chart_hour_hist()

        # Cập nhật mô tả biểu đồ
        desc = self._chart_descriptions().get(key, "")
        self.chart_hint_label.setText(desc)

        if chart_widget:
            self.chart_container_layout.addWidget(chart_widget)

    # Biểu đồ doanh thu theo tháng (Seaborn lineplot)
    def _chart_revenue_trend(self):
        figure = Figure(figsize=(5, 3.5))
        ax = figure.add_subplot(111)

        # Lấy dữ liệu từ controller
        months, revenues = self.controller.get_revenue_trend_data()

        if HAS_SEABORN:
            sns.lineplot(x=months, y=revenues, marker="o", ax=ax, color="#2E86C1")
        else:
            ax.plot(months, revenues, marker="o", color="#2E86C1")
        ax.set_title("Doanh Thu Tháng", fontsize=11)
        ax.set_ylabel("Triệu đồng")
        ax.set_xlabel("Tháng")
        ax.grid(True, alpha=0.3)

        return FigureCanvas(figure)

    # Biểu đồ cơ cấu lượt xe theo loại thẻ (Seaborn barplot)
    def _chart_vehicle_mix(self):
        figure = Figure(figsize=(5, 3.5))
        ax = figure.add_subplot(111)

        # Lấy dữ liệu từ controller
        labels, values = self.controller.get_vehicle_mix_data(self.start_date, self.end_date)

        if HAS_SEABORN:
            sns.barplot(x=labels, y=values, ax=ax, palette="Blues")
        else:
            ax.bar(labels, values, color="#3498DB")
        ax.set_title("Cơ Cấu Lượt Xe", fontsize=11)
        ax.set_ylabel("Số lượt")
        ax.set_xlabel("Nhóm khách")
        ax.tick_params(axis="x", rotation=0)

        return FigureCanvas(figure)

    # Boxplot thời gian đỗ theo loại xe (Seaborn boxplot)
    def _chart_duration_boxplot(self):
        figure = Figure(figsize=(5, 3.5))
        ax = figure.add_subplot(111)

        # Lấy dữ liệu từ controller
        samples = self.controller.get_duration_boxplot_data(self.start_date, self.end_date)

        labels = []
        durations = []
        for k, vals in samples.items():
            labels.extend([k] * len(vals))
            durations.extend(vals)

        if HAS_SEABORN:
            sns.boxplot(x=labels, y=durations, ax=ax, palette="Set2")
        else:
            # fallback đơn giản bằng scatter khi không có seaborn
            ax.scatter(labels, durations, alpha=0.6, color="#2ECC71")
        ax.set_title("Thời Gian Đỗ Xe Theo Nhóm", fontsize=11)
        ax.set_ylabel("Phút đỗ")
        ax.set_xlabel("Nhóm khách")
        ax.tick_params(axis="x", rotation=0)

        return FigureCanvas(figure)

    # Heatmap lượt xe theo giờ & ngày (Seaborn heatmap)
    def _chart_traffic_heatmap(self):
        figure = Figure(figsize=(5, 3.5))
        ax = figure.add_subplot(111)

        # Lấy dữ liệu từ controller
        days, hours, traffic = self.controller.get_traffic_heatmap_data(self.start_date, self.end_date)

        if HAS_SEABORN:
            sns.heatmap(
                traffic,
                annot=True,
                fmt="d",
                cmap="YlOrRd",
                xticklabels=hours,
                yticklabels=days,
                ax=ax,
            )
            ax.set_xlabel("Khung giờ")
            ax.set_ylabel("Ngày")
            ax.set_title("Mật Độ Lượt Xe Theo Giờ & Ngày", fontsize=11)
        else:
            ax.set_title("Cần cài seaborn để xem heatmap", fontsize=11)
            ax.axis("off")

        return FigureCanvas(figure)

    # Barplot lượt vào/ra theo ngày trong tuần
    def _chart_dow_entries(self):
        figure = Figure(figsize=(5, 3.5))
        ax = figure.add_subplot(111)

        # Lấy dữ liệu từ controller
        days, entries, exits = self.controller.get_dow_entries_data(self.start_date, self.end_date)

        if HAS_SEABORN:
            sns.barplot(x=days, y=entries, ax=ax, color="#3498DB", label="Vào", alpha=0.9)
            sns.barplot(x=days, y=exits, ax=ax, color="#2ECC71", label="Ra", alpha=0.7)
        else:
            ax.bar(days, entries, color="#3498DB", label="Vào")
            ax.bar(days, exits, color="#2ECC71", alpha=0.7, label="Ra")

        ax.set_title("Lượt Vào/Ra Theo Ngày", fontsize=11)
        ax.set_ylabel("Số lượt")
        ax.set_xlabel("Ngày")
        ax.legend()
        ax.tick_params(axis="x", rotation=0)
        ax.grid(True, alpha=0.2)
        return FigureCanvas(figure)

    # Scatter hồi quy phí vs thời gian đỗ
    def _chart_fee_vs_duration(self):
        figure = Figure(figsize=(5, 3.5))
        ax = figure.add_subplot(111)

        # Lấy dữ liệu từ controller
        duration, fee = self.controller.get_fee_vs_duration_data(self.start_date, self.end_date)

        if HAS_SEABORN:
            sns.regplot(x=duration, y=fee, ax=ax, scatter_kws={"alpha": 0.7}, line_kws={"color": "#E74C3C"})
        else:
            ax.scatter(duration, fee, alpha=0.7, color="#2980B9")
            # simple linear fit fallback
            if duration:
                m, b = 0.4, 7
                xs = [min(duration), max(duration)]
                ys = [m * x + b for x in xs]
                ax.plot(xs, ys, color="#E74C3C")

        ax.set_title("Tương Quan Phí vs Thời Gian Đỗ", fontsize=11)
        ax.set_xlabel("Phút đỗ")
        ax.set_ylabel("Phí (nghìn đồng)")
        ax.grid(True, alpha=0.2)
        return FigureCanvas(figure)

    # Histogram lượt xe theo giờ
    def _chart_hour_hist(self):
        figure = Figure(figsize=(5, 3.5))
        ax = figure.add_subplot(111)

        # Lấy dữ liệu từ controller
        hour_data = self.controller.get_hour_histogram_data(self.start_date, self.end_date)
        
        # Chuyển đổi sang list các giờ (0-23) với số lần xuất hiện
        hours = []
        for hour in range(24):
            hours.extend([hour] * hour_data[hour])

        if HAS_SEABORN:
            sns.histplot(hours, bins=24, ax=ax, color="#9B59B6", kde=True)
        else:
            ax.hist(hours, bins=24, color="#9B59B6", alpha=0.85)

        ax.set_title("Phân Bố Lượt Xe Theo Giờ", fontsize=11)
        ax.set_xlabel("Giờ trong ngày")
        ax.set_ylabel("Số lượt")
        ax.grid(True, alpha=0.2)
        return FigureCanvas(figure)
