"""
Base classes cho tất cả panels/tabs.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class BasePanel(QWidget):
    """
    Base class cho tất cả panels.
    
    Features:
    - Automatic layout setup
    - Title formatting
    - Common methods
    """
    
    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self.title_text = title
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(10)
        
        # Setup title if provided
        if title:
            self._setup_title()
        
        self._setupUi()
    
    def _setup_title(self):
        """Thêm title label với formatting"""
        title_label = QLabel(self.title_text)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 16, weight=QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2E86C1; margin-bottom: 10px;")
        self.main_layout.insertWidget(0, title_label)
    
    def _setupUi(self):
        """Override trong subclasses"""
        pass
    
    def add_widget(self, widget):
        """Add widget to layout"""
        self.main_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add layout to main layout"""
        self.main_layout.addLayout(layout)


class AdminTab(BasePanel):
    """Base class cho Admin tabs"""
    pass


class EmployeePanel(BasePanel):
    """Base class cho Employee panels"""
    def __init__(self, parent=None):
        super().__init__(parent, title="")
        # Override: Employee panels không dùng title chung
