from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget
from PyQt6.QtCore import Qt

from ui.admin.tabs.overviewTab import OverviewTab
from ui.admin.tabs.chartsTab import ChartsTab
from ui.admin.tabs.reportsTab import ReportsTab

try:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class StatsTab(QWidget):
    """Tab chính chứa các tab con: Tổng quan, Biểu đồ, và Báo cáo"""
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Khởi tạo giao diện chính với các tab con"""
        main_layout = QVBoxLayout()

        title = QLabel("THỐNG KÊ VÀ BÁO CÁO BÃI XE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:22px; font-weight:bold; color:#2E86C1; padding:10px;")
        main_layout.addWidget(title)

        stats_tabs = QTabWidget()

        # Tab Tổng Quan
        self.overview_tab = OverviewTab()
        stats_tabs.addTab(self.overview_tab, "Tổng Quan")

        # Tab Biểu Đồ (chỉ hiển thị nếu có matplotlib)
        if HAS_MATPLOTLIB:
            self.charts_tab = ChartsTab()
            stats_tabs.addTab(self.charts_tab, "Biểu Đồ")

        # Tab Báo Cáo Chi Tiết
        self.reports_tab = ReportsTab()
        stats_tabs.addTab(self.reports_tab, "Báo Cáo Chi Tiết")
        
        main_layout.addWidget(stats_tabs)
        self.setLayout(main_layout)
