from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from ui.admin.tabs.cardsSub import CardSubTabLuot, CardSubTabThang


class CardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.card_tabs = QTabWidget()
        self.card_tabs.addTab(CardSubTabLuot(), "Thẻ lượt")
        self.card_tabs.addTab(CardSubTabThang(), "Thẻ tháng")

        layout.addWidget(self.card_tabs)
        self.setLayout(layout)
