"""
Base classes cho tất cả main windows.
Tập trung style, title, và common functionality.
"""
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from ui.styles import getGlobalStyle


class BaseMainWindow(QMainWindow):
    """
    Base class cho tất cả main windows.
    
    Chứa:
    - Style chung (CSS)
    - Window title
    - Geometry mặc định
    """
    
    def __init__(self, title="Smart Parking System", width=1200, height=600):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, width, height)
        
        # Apply global style
        self.setStyleSheet(getGlobalStyle())
        
        # Optional: Đặt window center
        self._center_window()
    
    def _center_window(self):
        """Center window on screen"""
        from PyQt5.QtWidgets import QApplication
        desktop = QApplication.desktop()
        x = (desktop.width() - self.width()) // 2
        y = (desktop.height() - self.height()) // 2
        self.move(x, y)


class AdminMainWindow(BaseMainWindow):
    """Base class cho Admin windows"""
    def __init__(self):
        super().__init__(
            title="Hệ thống Quản Lý Bãi Xe - Admin",
            width=1200,
            height=600
        )


class EmployeeMainWindow(BaseMainWindow):
    """Base class cho Employee windows"""
    def __init__(self):
        super().__init__(
            title="Hệ thống Quản Lý Bãi Xe - Nhân Viên",
            width=1400,
            height=800
        )
