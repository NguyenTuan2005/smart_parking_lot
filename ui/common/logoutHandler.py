
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import pyqtSignal, QObject


class LogoutHandler(QObject):
    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def request_logout(self, window=None):
        if window:
            msg = QMessageBox(window)
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("Xác nhận đăng xuất")
            msg.setText("Bạn có chắc chắn muốn đăng xuất?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setDefaultButton(QMessageBox.StandardButton.No)
            
            # Apply clear styling to override global yellow buttons and faint text
            msg.setStyleSheet("""
                QMessageBox { background-color: white; }
                QLabel { color: #2c3e50; font-size: 13px; }
                QPushButton { 
                    background-color: #f0f0f0; color: #333; 
                    border: 1px solid #ccc; border-radius: 4px; 
                    padding: 5px 15px; min-width: 80px; 
                }
                QPushButton:hover { background-color: #e5f1fb; border: 1px solid #0078d7; }
            """)

            if msg.exec() == QMessageBox.StandardButton.Yes:
                window.close()
                self.logout_requested.emit()
        else:
            self.logout_requested.emit()

    def confirm_logout(self, window=None):
        if window:
            msg = QMessageBox(window)
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("Đăng xuất")
            msg.setText("Bạn muốn đăng xuất khỏi hệ thống?")
            msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg.setDefaultButton(QMessageBox.StandardButton.No)
            
            # Apply clear styling
            msg.setStyleSheet("""
                QMessageBox { background-color: white; }
                QLabel { color: #2c3e50; font-size: 13px; }
                QPushButton { 
                    background-color: #f0f0f0; color: #333; 
                    border: 1px solid #ccc; border-radius: 4px; 
                    padding: 5px 15px; min-width: 80px; 
                }
                QPushButton:hover { background-color: #e5f1fb; border: 1px solid #0078d7; }
            """)
            
            return msg.exec() == QMessageBox.StandardButton.Yes
        return True