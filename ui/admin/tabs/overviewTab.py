from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QGridLayout,
    QGraphicsDropShadowEffect,
    QPushButton,
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QIcon, QPixmap

from controllers.StatisticsController import StatisticsController

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Tahoma", "Roboto", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


class StatCard(QFrame):
    def __init__(self, title, value, icon_path, color_code, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(140)
        self.setMinimumWidth(280)
        self.setObjectName("StatCard")

        self.setStyleSheet(
            f"""
            QFrame#StatCard {{
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }}
            QLabel {{
                background: transparent;
            }}
        """
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        # Content Layout: Text (Left) + Icon (Right)
        content_layout = QHBoxLayout()

        # Text grouping
        text_group = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 14px; font-weight: 600;")
        text_group.addWidget(title_label)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(
            f"color: {color_code}; font-size: 32px; font-weight: bold; margin-top: 5px;"
        )
        text_group.addWidget(self.value_label)

        content_layout.addLayout(text_group, 1)

        # Icon on the right
        from PyQt6.QtGui import QPixmap

        icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon_label.setPixmap(
                pixmap.scaled(
                    60,
                    60,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        icon_label.setFixedSize(60, 60)
        content_layout.addWidget(
            icon_label, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )

        layout.addLayout(content_layout)

        layout.addStretch()

        # Add a subtle bottom indicator line
        line = QFrame()
        line.setFixedHeight(4)
        line.setStyleSheet(f"background-color: {color_code}; border-radius: 2px;")
        layout.addWidget(line)


class QuickStatsItem(QFrame):
    def __init__(self, title, value, icon_path, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(85)
        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #f0f0f0;
                border-radius: 12px;
            }
        """
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # Icon
        icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon_label.setPixmap(
                pixmap.scaled(
                    40,
                    40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        icon_label.setFixedSize(40, 40)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(
            "color: #7f8c8d; font-size: 14px; font-weight: 600; border: none; background: transparent;"
        )
        self.value_lbl = QLabel(value)
        self.value_lbl.setStyleSheet(
            "color: black; font-size: 18px; font-weight: bold; border: none; background: transparent;"
        )

        text_layout.addWidget(title_lbl)
        text_layout.addWidget(self.value_lbl)

        layout.addLayout(text_layout)
        layout.addStretch()


class OverviewTab(QWidget):

    def __init__(self):
        super().__init__()
        self.stats_controller = StatisticsController(self)
        self.start_date = None
        self.end_date = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        # Header Section
        header_layout = QHBoxLayout()
        title_label = QLabel("TỔNG QUAN HỆ THỐNG")
        title_label.setStyleSheet(
            "font-size: 24px; font-weight: 800; color: #2e86c1; padding-left: 15px"
        )
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Refresh Section: Time Label + Reload Button
        refresh_layout = QHBoxLayout()
        refresh_layout.setSpacing(15)

        self.lbl_last_update = QLabel("Cập nhật lần cuối: --:--")
        self.lbl_last_update.setStyleSheet("color: #95a5a6; font-size: 13px;")

        self.btn_reload = QPushButton(" Làm mới")
        self.btn_reload.setIcon(QIcon("assets/icons/refresh.png"))
        self.btn_reload.setIconSize(QSize(16, 16))
        self.btn_reload.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_reload.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                padding: 8px 18px;
                color: #2c3e50;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #3498db;
                color: #3498db;
            }
            QPushButton:pressed {
                background-color: #ecf0f1;
            }
        """
        )

        refresh_layout.addWidget(self.lbl_last_update)
        refresh_layout.addWidget(self.btn_reload)
        header_layout.addLayout(refresh_layout)

        layout.addLayout(header_layout)

        # 1. Stat Cards Row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(25)

        self.card_revenue = StatCard(
            "Doanh thu hôm nay", "0 ₫", "assets/icons/revenue.png", "#27ae60"
        )
        self.card_parked = StatCard(
            "Xe đang gửi", "0", "assets/icons/motorbike.png", "#2980b9"
        )
        self.card_entries = StatCard(
            "Lượt xe hôm nay", "0", "assets/icons/bikeCount.png", "#27ae60"
        )
        self.card_monthly = StatCard(
            "Thẻ tháng còn hạn", "0", "assets/icons/card.png", "#2980b9"
        )

        cards_layout.addWidget(self.card_revenue, 1)
        cards_layout.addWidget(self.card_parked, 1)
        cards_layout.addWidget(self.card_entries, 1)
        cards_layout.addWidget(self.card_monthly, 1)

        layout.addLayout(cards_layout)
        layout.addSpacing(8)

        # 2. Main Content: Revenue Chart and Quick Stats
        main_content_layout = QHBoxLayout()
        main_content_layout.setSpacing(25)

        # Chart Container
        self.chart_frame = QFrame()
        self.chart_frame.setObjectName("ChartFrame")
        self.chart_frame.setStyleSheet(
            """
            QFrame#ChartFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
        """
        )
        self.chart_layout = QVBoxLayout(self.chart_frame)
        self.chart_layout.setContentsMargins(15, 15, 15, 15)

        # Add shadow to chart frame
        chart_shadow = QGraphicsDropShadowEffect(self.chart_frame)
        chart_shadow.setBlurRadius(15)
        chart_shadow.setXOffset(0)
        chart_shadow.setYOffset(4)
        chart_shadow.setColor(QColor(0, 0, 0, 40))
        self.chart_frame.setGraphicsEffect(chart_shadow)

        main_content_layout.addWidget(self.chart_frame, 3)

        # Update chart content initially
        self._update_revenue_chart()

        # Quick Stats Panel
        stats_panel = QFrame()
        stats_panel.setObjectName("StatsPanel")
        stats_panel.setStyleSheet(
            """
            QFrame#StatsPanel {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #e0e0e0;
            }
        """
        )

        stats_layout = QVBoxLayout(stats_panel)
        stats_layout.setContentsMargins(20, 20, 20, 20)
        stats_layout.setSpacing(15)

        stats_header = QLabel("Thống kê trong ngày")
        stats_header.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 5px;"
        )
        stats_layout.addWidget(stats_header)

        # Items
        self.stat_overnight = QuickStatsItem(
            "Xe qua đêm", "15", "assets/icons/motorbike.png"
        )
        self.stat_expiring = QuickStatsItem(
            "Thẻ sắp hết hạn", "4", "assets/icons/card.png"
        )
        self.stat_active_cams = QuickStatsItem(
            "Camera hoạt động", "1 / 1", "assets/icons/camera.png"
        )

        stats_layout.addWidget(self.stat_overnight)
        stats_layout.addWidget(self.stat_expiring)
        stats_layout.addWidget(self.stat_active_cams)
        stats_layout.addStretch()

        # Add shadow to stats panel
        stats_shadow = QGraphicsDropShadowEffect(stats_panel)
        stats_shadow.setBlurRadius(15)
        stats_shadow.setXOffset(0)
        stats_shadow.setYOffset(4)
        stats_shadow.setColor(QColor(0, 0, 0, 40))
        stats_panel.setGraphicsEffect(stats_shadow)

        main_content_layout.addWidget(stats_panel, 1)

        layout.addLayout(main_content_layout, 2)  # Higher stretch factor for content

        self.update_stats(0, 0, 0, 0)

    def _create_figure(self, figsize=(10, 6)):
        figure = Figure(figsize=figsize, dpi=100)
        figure.subplots_adjust(left=0.1, right=0.95, top=0.90, bottom=0.15)
        return figure

    def _chart_revenue_trend(self):

        figure = self._create_figure()
        ax = figure.add_subplot(111)

        # Lấy dữ liệu doanh thu theo ngày trong tháng hiện tại
        days, revenues = self.stats_controller.get_daily_revenue_data()

        sns.lineplot(
            x=days, y=revenues, marker="o", ax=ax, color="#2E86C1", linewidth=2.5
        )
        try:
            ax.fill_between(days, revenues, color="#2E86C1", alpha=0.1)
        except:
            pass

        # Optimize x-axis labels
        import matplotlib.ticker as ticker

        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True, nbins=15))

        ax.set_title(
            "Doanh Thu Theo Ngày (Tháng Hiện Tại)",
            fontsize=12,
            fontweight="bold",
            pad=20,
            color="#2c3e50",
            fontname="Arial",
        )
        ax.set_ylabel("Nghìn đồng", fontsize=10, color="#7f8c8d", fontname="Arial")
        ax.set_xlabel(
            "Ngày trong tháng", fontsize=10, color="#7f8c8d", fontname="Arial"
        )
        ax.grid(True, alpha=0.2, linestyle="--")
        ax.tick_params(axis="x", rotation=0, labelsize=9)
        ax.tick_params(axis="y", labelsize=9)

        # Clean up layout
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        return FigureCanvas(figure)

    def _update_revenue_chart(self):
        # Clear old chart
        while self.chart_layout.count():
            item = self.chart_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add new chart
        chart_widget = self._chart_revenue_trend()
        if chart_widget:
            self.chart_layout.addWidget(chart_widget)

    def update_stats(
        self, revenue, parked, entries, monthly, overnight=0, expiring=0, cameras=0
    ):
        self.card_revenue.value_label.setText(f"{int(revenue):,} ₫")
        self.card_parked.value_label.setText(str(parked))
        self.card_entries.value_label.setText(str(entries))
        self.card_monthly.value_label.setText(str(monthly))

        # Cập nhật bảng thống kê nhanh
        self.stat_overnight.value_lbl.setText(str(overnight))
        self.stat_expiring.value_lbl.setText(str(expiring))
        self.stat_active_cams.value_lbl.setText(
            f"{cameras} / {cameras}"
        )  # Giả định tất cả camera trong DB là online

        # Cũng cập nhật luôn biểu đồ khi reload
        self._update_revenue_chart()

        from datetime import datetime

        self.lbl_last_update.setText(
            f"Cập nhật lúc: {datetime.now().strftime('%H:%M:%S')}"
        )
