from services.ReportsService import ReportService
from PyQt6.QtCore import QDate


class ReportController:
    def __init__(self, stats_tab):
        self.stats_tab = stats_tab
        self.reports_view = stats_tab.reports_tab
        self.overview_view = stats_tab.overview_tab
        self.service = ReportService()

        if hasattr(self.reports_view, 'btn_apply'):
            self.reports_view.btn_apply.clicked.connect(self.load_report_data)
        if hasattr(self.reports_view, 'btn_today'):
            self.reports_view.btn_today.clicked.connect(self.set_report_today)

        # Connect Refresh button in Overview
        if hasattr(self.overview_view, 'btn_reload'):
            self.overview_view.btn_reload.clicked.connect(self.refresh_overview)

        # Timer to refresh overview every 60 seconds
        from PyQt6.QtCore import QTimer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_overview)
        self.refresh_timer.start(60000) # 60 seconds

        self.load_report_default_data()
        self.refresh_overview()

    def load_report_default_data(self):
        start_date = QDate(2024, 1, 1)
        end_date = QDate.currentDate()

        if hasattr(self.reports_view, 'start_date_input'):
            self.reports_view.start_date_input.setDate(start_date)
        if hasattr(self.reports_view, 'end_date_input'):
            self.reports_view.end_date_input.setDate(end_date)

        self.load_report_data()

    def load_report_data(self):
        if not hasattr(self.reports_view, 'start_date_input'):
            return
            
        start = self.reports_view.start_date_input.date().toPyDate()
        end = self.reports_view.end_date_input.date().toPyDate()

        data = self.service.get_report_data(start, end)
        self.reports_view.update_ui(data)

    def set_report_today(self):
        today = QDate.currentDate()
        self.reports_view.start_date_input.setDate(today)
        self.reports_view.end_date_input.setDate(today)
        self.load_report_data()

    def refresh_overview(self):
        stats = self.service.get_overview_stats()
        self.overview_view.update_stats(
            revenue=stats["revenue"],
            parked=stats["parked"],
            entries=stats["entries"],
            monthly=stats["monthly"]
        )
