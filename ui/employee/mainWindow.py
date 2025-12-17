from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMenuBar
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QAction

from controllers.StaffController import StaffController
from ui.employee.leftPanel import LeftPanel
from ui.employee.centerPanel import CenterPanel
from ui.employee.rightPanel import RightPanel
from ui.styles import getGlobalStyle
from ui.common import LogoutHandler


class EmployeeMainWindow(QMainWindow):
    """
    Lớp chính cho Giao diện Hệ thống Quản lý Bãi đỗ xe cho Nhân viên (QMainWindow).
    Tích hợp các panel (Left, Center, Right).
    """
    logout_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống Quản lý - Nhân viên")
        self.setGeometry(100, 100, 1400, 800)
        self.__controller = StaffController()

        # Áp dụng Global Style
        self.setStyleSheet(getGlobalStyle())
        
        self.logout_handler = LogoutHandler(self)
        self.logout_handler.logout_requested.connect(self._on_logout)

        self._createMenuBar()
        self._setupMainLayout()


    def _createMenuBar(self):
        """
        Tạo thanh Menu bar ở trên cùng với các thành phần cụ thể (Cho Nhân viên).
        """
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        # --- 1. Menu "Hệ thống" ---
        systemMenu = menuBar.addMenu("Hệ thống")
        
        logout_action = QAction("Đăng xuất", self)
        logout_action.triggered.connect(self._request_logout)
        systemMenu.addAction(logout_action)
        
        systemMenu.addSeparator()  # Thêm đường phân cách
        
        exit_action = QAction("Thoát", self)
        exit_action.triggered.connect(self.close)
        systemMenu.addAction(exit_action)

        # --- 3. Menu "Hỗ trợ" ---
        support_menu = menuBar.addMenu("Hỗ trợ")
        support_menu.addAction(QAction("Về chúng tôi", self))
        support_menu.addAction(QAction("Trợ giúp", self))

    def _request_logout(self):
        """Xử lý yêu cầu đăng xuất"""
        if self.logout_handler.confirm_logout(self):
            self.logout_requested.emit()
            self.close()

    def _on_logout(self):
        """Callback khi đăng xuất"""
        pass

    def _setupMainLayout(self):
        """
        Thiết lập Central Widget và Layout chính (QHBoxLayout).
        """
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QHBoxLayout(centralWidget)
        mainLayout.setContentsMargins(5, 5, 5, 5)
        mainLayout.setSpacing(10)

        # 1. Cột Trái (Left Pane) - Sử dụng lớp LeftPanel
        leftPane = LeftPanel(self.__controller)
        mainLayout.addWidget(leftPane, 1)  # Tỉ lệ 1 (cột hẹp)

        # 2. Cột Giữa (Center Pane) - Sử dụng lớp CenterPanel
        centerPane = CenterPanel(self.__controller)
        mainLayout.addWidget(centerPane, 4)  # Tỉ lệ 4 (cột rộng nhất)

        # 3. Cột Phải (Right Pane) - Sử dụng lớp RightPanel
        rightPane = RightPanel(self.__controller)
        mainLayout.addWidget(rightPane, 2)  # Tỉ lệ 2 (cột trung bình)
