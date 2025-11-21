from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMenuBar, QAction
from PyQt6.QtCore import Qt, QSize
# Import các Panel đã chia nhỏ
from LeftPanel import LeftPanel
from CenterPanel import CenterPanel
from RightPanel import RightPanel
from Styles import getGlobalStyle  # Import hàm style


class MenuMain(QMainWindow):
    """
    Lớp chính cho Giao diện Hệ thống Quản lý Bãi đỗ xe (QMainWindow).
    Tích hợp các panel (Left, Center, Right).
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ thống Quản lý")
        self.setGeometry(100, 100, 1400, 800)

        # Áp dụng Global Style
        self.setStyleSheet(getGlobalStyle())

        self._createMenuBar()
        self._setupMainLayout()

    def _createMenuBar(self):
        """
        Tạo thanh Menu bar ở trên cùng với các thành phần cụ thể.
        """
        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)

        # --- 1. Menu "Hệ thống" ---
        systemMenu = menuBar.addMenu("Hệ thống")
        systemMenu.addAction(QAction("Cấu hình cổng", self))
        systemMenu.addAction(QAction("Quản lý người dùng", self))
        systemMenu.addSeparator()  # Thêm đường phân cách
        systemMenu.addAction(QAction("Đăng xuất", self))

        # --- 2. Menu "Quản lý" ---
        managementMenu = menuBar.addMenu("Quản lý")
        managementMenu.addAction(QAction("Danh sách vé tháng", self))
        managementMenu.addAction(QAction("Báo cáo", self))
        managementMenu.addSeparator()
        managementMenu.addAction(QAction("Theo dõi sự kiện", self))

        # --- 3. Menu "HÌNH ẢNH" ---
        menuBar.addAction(QAction("Hình ảnh", self))

        # --- 4. Menu "Hỗ trợ" ---
        support_menu = menuBar.addMenu("Hỗ trợ")
        support_menu.addAction(QAction("Về chúng tôi", self))
        support_menu.addAction(QAction("Trợ giúp", self))

        # --- 5. Menu "Style" (Theme) ---
        style_menu = menuBar.addMenu("Style")
        style_menu.addAction(QAction("Dark", self))


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
        leftPane = LeftPanel()
        mainLayout.addWidget(leftPane, 1)  # Tỉ lệ 1 (cột hẹp)

        # 2. Cột Giữa (Center Pane) - Sử dụng lớp CenterPanel
        centerPane = CenterPanel()
        mainLayout.addWidget(centerPane, 4)  # Tỉ lệ 4 (cột rộng nhất)

        # 3. Cột Phải (Right Pane) - Sử dụng lớp RightPanel
        rightPane = RightPanel()
        mainLayout.addWidget(rightPane, 2)  # Tỉ lệ 2 (cột trung bình)
