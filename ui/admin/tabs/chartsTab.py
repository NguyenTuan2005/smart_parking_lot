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
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        subtitle = QLabel("BIỂU ĐỒ THỐNG KÊ")
        subtitle.setStyleSheet("font-size:24px; font-weight:bold; color:#2e86c1;")
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
        # Tăng padding top để tránh cắt tiêu đề, tăng bottom để tránh che chú thích
        figure.subplots_adjust(left=0.1, right=0.95, top=0.90, bottom=0.25)
        return figure

    def _chart_revenue_trend(self):
        """Biểu đồ doanh thu theo tháng - Đã cải tiến"""
        figure = self._create_figure()
        ax = figure.add_subplot(111)

        months, revenues = self.controller.get_revenue_trend_data(
            start_date=self.start_date, end_date=self.end_date
        )

        # Lọc chỉ các tháng có dữ liệu trong khoảng thời gian được chọn
        if self.start_date and self.end_date:
            filtered_months = []
            filtered_revenues = []
            month_names = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"]

            for i, (month, revenue) in enumerate(zip(months, revenues)):
                month_num = i + 1
                # Kiểm tra tháng có nằm trong khoảng thời gian không
                if self.start_date.month <= month_num <= self.end_date.month or revenue > 0:
                    filtered_months.append(month)
                    filtered_revenues.append(revenue)

            months = filtered_months if filtered_months else months
            revenues = filtered_revenues if filtered_revenues else revenues

        if HAS_SEABORN:
            sns.lineplot(x=months, y=revenues, marker="o", ax=ax, color="#2E86C1",
                         linewidth=2.5, markersize=8)
        else:
            ax.plot(months, revenues, marker="o", color="#2E86C1", linewidth=2.5, markersize=8)

        # Chú thích giá trị với định dạng rõ ràng hơn
        for i, (month, revenue) in enumerate(zip(months, revenues)):
            if revenue > 0:  # Chỉ hiển thị cho tháng có doanh thu
                ax.annotate(f'{revenue:.1f}k',
                            xy=(month, revenue),
                            xytext=(0, 8),
                            textcoords='offset points',
                            fontsize=9,
                            color='#2E86C1',
                            fontweight='bold',
                            ha='center',
                            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                                      edgecolor='#2E86C1', alpha=0.9))

        # Thông tin tổng quan với thống kê bổ sung
        total_revenue = sum(revenues)
        avg_revenue = total_revenue / len([r for r in revenues if r > 0]) if any(revenues) else 0
        max_revenue = max(revenues) if revenues else 0

        stats_text = f'Tổng: {total_revenue:.1f}k | TB: {avg_revenue:.1f}k | Cao nhất: {max_revenue:.1f}k'
        ax.text(0.98, 0.98, stats_text,
                transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF3CD',
                          edgecolor='#FFC107', alpha=0.9))

        ax.set_title("Doanh Thu Theo Tháng", fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel("Nghìn đồng (k)", fontsize=12, fontweight='bold')
        ax.set_xlabel("Tháng", fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.tick_params(axis='y', labelsize=10)

        # Định dạng trục y để hiển thị số đẹp hơn
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:.0f}k'))

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
        """Heatmap lượt xe theo giờ & ngày - Đã cải tiến"""
        figure = self._create_figure(figsize=(14, 7))
        # Tăng bottom margin cho heatmap để có chỗ cho chú thích
        figure.subplots_adjust(left=0.1, right=0.95, top=0.90, bottom=0.25)
        ax = figure.add_subplot(111)

        days, hours, traffic = self.controller.get_traffic_heatmap_data(
            self.start_date, self.end_date
        )

        if HAS_SEABORN:
            # Tính tổng để làm màu sáng/tối phù hợp
            max_traffic = max(max(row) for row in traffic) if traffic else 1

            sns.heatmap(
                traffic,
                annot=True,
                fmt="d",
                cmap="RdYlGn_r",  # Đỏ = cao điểm, Xanh = ít xe
                xticklabels=hours,
                yticklabels=days,
                ax=ax,
                cbar_kws={'label': 'Số lượt xe', 'shrink': 0.8},
                linewidths=0.5,
                linecolor='gray',
                vmin=0,
                vmax=max_traffic,
                annot_kws={'fontsize': 10, 'fontweight': 'bold'}
            )

            ax.set_xlabel("Khung giờ", fontsize=12, fontweight='bold')
            ax.set_ylabel("Ngày trong tuần", fontsize=12, fontweight='bold')
            ax.set_title("Mật Độ Lượt Xe Theo Giờ & Ngày", fontsize=16, fontweight='bold', pad=15)

            # Thêm chú thích hướng dẫn
            total_vehicles = sum(sum(row) for row in traffic)
            ax.text(0.5, -0.25, f'Tổng số lượt: {total_vehicles} | Màu đậm = Cao điểm',
                    transform=ax.transAxes, fontsize=10, ha='center',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.7))
        else:
            ax.set_title("Cần cài seaborn để xem heatmap", fontsize=14)
            ax.axis("off")

        return FigureCanvas(figure)

    def _chart_dow_entries(self):
        """Biểu đồ lượt vào/ra theo ngày - Đã cải tiến"""
        figure = self._create_figure()
        ax = figure.add_subplot(111)

        days, entries, exits = self.controller.get_dow_entries_data(
            self.start_date, self.end_date
        )

        x = range(len(days))
        width = 0.38

        bars1 = ax.bar([i - width / 2 for i in x], entries, width,
                       label='Vào', color='#3498DB', alpha=0.85, edgecolor='#2874A6', linewidth=1.5)
        bars2 = ax.bar([i + width / 2 for i in x], exits, width,
                       label='Ra', color='#2ECC71', alpha=0.85, edgecolor='#239B56', linewidth=1.5)

        # Chú thích giá trị trên mỗi bar với điều kiện
        for bar in bars1:
            height = bar.get_height()
            if height > 0:  # Chỉ hiển thị nếu có giá trị
                ax.text(bar.get_x() + bar.get_width() / 2., height + max(entries) * 0.02,
                        f'{int(height)}', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color='#2874A6')

        for bar in bars2:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width() / 2., height + max(exits) * 0.02,
                        f'{int(height)}', ha='center', va='bottom',
                        fontsize=9, fontweight='bold', color='#239B56')

        # Thêm đường trung bình
        avg_entries = sum(entries) / len(entries) if entries else 0
        avg_exits = sum(exits) / len(exits) if exits else 0
        ax.axhline(y=avg_entries, color='#3498DB', linestyle='--',
                   linewidth=1.5, alpha=0.5, label=f'TB Vào: {avg_entries:.0f}')
        ax.axhline(y=avg_exits, color='#2ECC71', linestyle='--',
                   linewidth=1.5, alpha=0.5, label=f'TB Ra: {avg_exits:.0f}')

        # Tìm ngày cao điểm
        max_entry_day = days[entries.index(max(entries))] if entries else ""
        max_exit_day = days[exits.index(max(exits))] if exits else ""

        # Thêm thống kê tổng quan ở góc phải trên
        total_entries = sum(entries)
        total_exits = sum(exits)
        ratio_text = f'Tổng vào: {total_entries} | Tổng ra: {total_exits}'
        ax.text(0.98, 0.98, ratio_text,
                transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#D5F4E6',
                          edgecolor='#27AE60', alpha=0.9))

        ax.set_title("Lượt Vào/Ra Theo Ngày Trong Tuần", fontsize=16, fontweight='bold', pad=15)
        ax.set_ylabel("Số lượt", fontsize=12, fontweight='bold')
        ax.set_xlabel("Ngày", fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(days, fontsize=11, fontweight='bold')
        ax.legend(fontsize=10, loc='lower right', framealpha=0.9)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.7)

        # Thêm chú thích ngày cao điểm
        if max_entry_day and max_exit_day:
            peak_text = f'Cao điểm vào: {max_entry_day} | Cao điểm ra: {max_exit_day}'
            ax.text(0.5, -0.25, peak_text,
                    transform=ax.transAxes, fontsize=10, ha='center',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFE5E5',
                              edgecolor='#E74C3C', alpha=0.8))

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
        """Biểu đồ phân bố lượt xe theo giờ - Đã cải tiến"""
        figure = self._create_figure()
        ax = figure.add_subplot(111)

        hour_data = self.controller.get_hour_histogram_data(
            self.start_date, self.end_date
        )

        hours = list(range(24))

        if HAS_SEABORN:
            # Tạo data frame cho seaborn
            hours_expanded = []
            for hour in range(24):
                hours_expanded.extend([hour] * hour_data[hour])

            if hours_expanded:  # Nếu có dữ liệu
                sns.histplot(hours_expanded, bins=24, ax=ax, color="#9B59B6",
                             kde=True, line_kws={"linewidth": 2.5, "color": "#7D3C98"},
                             edgecolor='#6C3483', linewidth=1.2)
            else:  # Nếu không có dữ liệu, vẽ bar chart trống
                ax.bar(hours, hour_data, color="#9B59B6", alpha=0.85,
                       edgecolor='#6C3483', linewidth=1.2)
        else:
            ax.bar(hours, hour_data, color="#9B59B6", alpha=0.85,
                   edgecolor='#6C3483', linewidth=1.2)

        # Chú thích giá trị chỉ cho các giờ có lượt xe > 0
        max_count = max(hour_data) if hour_data else 1
        for i, count in enumerate(hour_data):
            if count > 0:
                ax.text(i, count + max_count * 0.02, f'{count}',
                        ha='center', va='bottom', fontsize=8,
                        fontweight='bold', color='#6C3483')

        # Phân tích giờ cao điểm
        peak_hours = [h for h, c in enumerate(hour_data) if c == max(hour_data)]
        low_hours = [h for h, c in enumerate(hour_data) if c == min(hour_data) and c > 0]

        total_vehicles = sum(hour_data)
        avg_per_hour = total_vehicles / 24 if total_vehicles > 0 else 0

        # Đánh dấu giờ cao điểm
        for peak_hour in peak_hours:
            ax.axvline(x=peak_hour, color='#E74C3C', linestyle='--',
                       linewidth=2, alpha=0.7, label=f'Cao điểm: {peak_hour}h' if peak_hour == peak_hours[0] else '')

        # Đường trung bình
        ax.axhline(y=avg_per_hour, color='#3498DB', linestyle='--',
                   linewidth=1.5, alpha=0.6, label=f'Trung bình: {avg_per_hour:.1f}')

        ax.set_title("Phân Bố Lượt Xe Theo Giờ", fontsize=16, fontweight='bold', pad=15)
        ax.set_xlabel("Giờ trong ngày", fontsize=12, fontweight='bold')
        ax.set_ylabel("Số lượt xe", fontsize=12, fontweight='bold')
        ax.set_xticks(range(0, 24, 2))
        ax.set_xticklabels([f'{h}h' for h in range(0, 24, 2)], fontsize=10)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--', linewidth=0.7)
        ax.legend(fontsize=10, loc='upper right', framealpha=0.9)

        # Thêm thông tin phân tích
        if peak_hours and low_hours:
            peak_str = ', '.join([f'{h}h' for h in peak_hours[:3]])  # Lấy tối đa 3 giờ
            analysis_text = f'Tổng: {total_vehicles} lượt | Cao điểm: {peak_str}'
            ax.text(0.5, -0.25, analysis_text,
                    transform=ax.transAxes, fontsize=10, ha='center',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8DAEF',
                              edgecolor='#9B59B6', alpha=0.8))

        return FigureCanvas(figure)