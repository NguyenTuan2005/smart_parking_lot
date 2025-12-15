from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from ui.admin.tabs.cardsSub import MonthlyCardLogTab, SingleCardLogTab


class CardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.card_tabs = QTabWidget()

        self.single_card_tab = SingleCardLogTab()
        self.monthly_card_tab = MonthlyCardLogTab()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.card_tabs.addTab(self.single_card_tab, "Thẻ lượt")
        self.card_tabs.addTab(self.monthly_card_tab, "Thẻ tháng")

        layout.addWidget(self.card_tabs)
        self.setLayout(layout)

