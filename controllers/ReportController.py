from services.ReportsService import ReportService
from PyQt6.QtCore import QDate


class ReportController:
    def __init__(self, view):
        self.view = view
        self.service = ReportService()

        # CONNECT BUTTONS
        self.view.btn_apply.clicked.connect(self.load_data)
        self.view.btn_today.clicked.connect(self.set_today)

        # LOAD DEFAULT DATA
        self.load_default_data()

    def load_default_data(self):
        # Để chắc chắn có dữ liệu
        start_date = QDate(2024, 1, 1)
        end_date = QDate.currentDate()

        self.view.start_date_input.setDate(start_date)
        self.view.end_date_input.setDate(end_date)

        self.load_data()

    def load_data(self):
        start = self.view.start_date_input.date().toPyDate()
        end = self.view.end_date_input.date().toPyDate()

        print(f"[CONTROLLER] Load data from {start} to {end}")

        data = self.service.get_report_data(start, end)
        self.view.update_ui(data)

    def set_today(self):
        today = QDate.currentDate()
        self.view.start_date_input.setDate(today)
        self.view.end_date_input.setDate(today)
        self.load_data()
