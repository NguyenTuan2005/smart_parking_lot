from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, 
    QGraphicsDropShadowEffect, QPushButton
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QIcon, QPixmap


class StatCard(QFrame):
    def __init__(self, title, value, icon_path, color_code, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(140)
        self.setMinimumWidth(280)
        self.setObjectName("StatCard")
        
        self.setStyleSheet(f"""
            QFrame#StatCard {{
                background-color: white;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }}
            QLabel {{
                background: transparent;
            }}
        """)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Content Layout: Text (Left) + Icon (Right)
        content_layout = QHBoxLayout()
        
        # Text grouping
        text_group = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 14px; font-weight: 600;")
        text_group.addWidget(title_label)
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"color: {color_code}; font-size: 32px; font-weight: bold; margin-top: 5px;")
        text_group.addWidget(self.value_label)
        
        content_layout.addLayout(text_group, 1)
        
        # Icon on the right
        from PyQt6.QtGui import QPixmap
        icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            icon_label.setPixmap(pixmap.scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setFixedSize(60, 60)
        content_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(content_layout)
        
        layout.addStretch()
        
        # Add a subtle bottom indicator line
        line = QFrame()
        line.setFixedHeight(4)
        line.setStyleSheet(f"background-color: {color_code}; border-radius: 2px;")
        layout.addWidget(line)


class OverviewTab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header Section
        header_layout = QHBoxLayout()
        title_label = QLabel("TỔNG QUAN HỆ THỐNG")
        title_label.setStyleSheet("font-size: 25px; font-weight: bold; color: #2e86c1")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Refresh Section: Time Label + Reload Button
        refresh_layout = QHBoxLayout()
        refresh_layout.setSpacing(15)
        
        self.lbl_last_update = QLabel("Cập nhật lúc: --:--")
        self.lbl_last_update.setStyleSheet("color: #95a5a6; font-size: 13px;")
        
        self.btn_reload = QPushButton(" Làm mới")
        self.btn_reload.setIcon(QIcon("assets/icons/refresh.png"))
        self.btn_reload.setIconSize(QSize(16, 16))
        self.btn_reload.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                padding: 6px 15px;
                color: #2c3e50;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #2e86c1;
            }
        """)
        
        refresh_layout.addWidget(self.lbl_last_update)
        refresh_layout.addWidget(self.btn_reload)
        header_layout.addLayout(refresh_layout)
        
        layout.addLayout(header_layout)
        
        # Stat Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(25)
        
        self.card_revenue = StatCard("Doanh thu hôm nay", "0 ₫", "assets/icons/revenue.png", "#27ae60")
        self.card_parked = StatCard("Xe đang gửi", "0", "assets/icons/motorbike.png", "#2980b9")
        self.card_entries = StatCard("Lượt xe hôm nay", "0", "assets/icons/bikeCount.png", "#f39c12")
        self.card_monthly = StatCard("Thẻ tháng còn hạn", "0", "assets/icons/card.png", "#324d8f")
        
        cards_layout.addWidget(self.card_revenue, 1)
        cards_layout.addWidget(self.card_parked, 1)
        cards_layout.addWidget(self.card_entries, 1)
        cards_layout.addWidget(self.card_monthly, 1)
        
        layout.addLayout(cards_layout)
        
        # Chart
        insight_layout = QHBoxLayout()
        
        info_frame = QFrame()
        insight_layout.addWidget(info_frame, 1)
        

        placeholder = QFrame()
        insight_layout.addWidget(placeholder, 2)
        
        layout.addLayout(insight_layout, 1)
        
        # Spacer at bottom
        layout.addStretch()

    def update_stats(self, revenue, parked, entries, monthly):
        self.card_revenue.value_label.setText(f"{int(revenue):,} ₫")
        self.card_parked.value_label.setText(str(parked))
        self.card_entries.value_label.setText(str(entries))
        self.card_monthly.value_label.setText(str(monthly))
        
        from datetime import datetime
        self.lbl_last_update.setText(f"Cập nhật lúc: {datetime.now().strftime('%H:%M:%S')}")
