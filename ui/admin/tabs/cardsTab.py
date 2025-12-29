from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from ui.admin.tabs.cardSubTab import MonthlyCardLogTab, SingleCardLogTab, SingleCardManagementTab


class CardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.card_tabs = QTabWidget()

        self.single_card_tab = SingleCardLogTab()
        self.single_card_management_tab = SingleCardManagementTab()
        self.monthly_card_tab = MonthlyCardLogTab()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.card_tabs.addTab(self.single_card_tab, "Nhật ký thẻ lượt")
        self.card_tabs.addTab(self.single_card_management_tab, "Quản lý thẻ lượt")
        self.card_tabs.addTab(self.monthly_card_tab, "Thẻ tháng")

        layout.addWidget(self.card_tabs)
        self.setLayout(layout)

