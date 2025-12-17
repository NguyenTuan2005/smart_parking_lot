import sys

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QMenuBar, QApplication
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction

from controllers.CardController import MonthlyCardController
from services.Session import Session
from ui.admin.tabs.cardsTab import CardTab
from ui.admin.tabs.customersTab import CustomerTab
from ui.admin.tabs.vehiclesTab import VehicleTab
from ui.admin.tabs.statsTab import StatsTab
from ui.admin.tabs.parkingConfigTab import ParkingConfigTab
from ui.common import LogoutHandler


class ParkingManagementApp(QMainWindow):
    logout_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.card_tab =CardTab()
        self.customer_tab = CustomerTab()
        self.vehicle_tab = VehicleTab()
        self.stats_tab = StatsTab()
        self.parking_config_tab = ParkingConfigTab()

        self.setWindowTitle("Hệ thống quản lý bãi xe - Admin")
        self.setGeometry(200, 100, 1200, 600)
        
        self.logout_handler = LogoutHandler(self)
        self.logout_handler.logout_requested.connect(self._on_logout)
        
        self._create_menu_bar()
        self.initUI()
        self._init_controllers()

    def _create_menu_bar(self):
        """Tạo menu bar với nút đăng xuất"""
        menubar = self.menuBar()
        
        # Menu Hệ thống
        system_menu = menubar.addMenu("Hệ thống")
        
        logout_action = QAction("Đăng xuất", self)
        logout_action.triggered.connect(self._request_logout)
        system_menu.addAction(logout_action)
        
        system_menu.addSeparator()
        
        exit_action = QAction("Thoát", self)
        exit_action.triggered.connect(self.close)
        system_menu.addAction(exit_action)

    def _request_logout(self):
        """Xử lý yêu cầu đăng xuất"""
        if self.logout_handler.confirm_logout(self):
            self.logout_requested.emit()
            self.close()

    def _on_logout(self):

        pass

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()

        self.tabs.addTab(self.card_tab, "Quản lý thẻ")
        self.tabs.addTab(self.customer_tab, "Quản lý khách hàng")
        self.tabs.addTab(self.vehicle_tab, "Quản lý phương tiện")
        self.tabs.addTab(self.stats_tab, "Thống kê")
        self.tabs.addTab(self.parking_config_tab, "Cấu hình bãi xe")

        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)

    def _init_controllers(self):
        self.card_controller = MonthlyCardController(
            view=self.card_tab.monthly_card_tab)