from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QHBoxLayout, QMessageBox, \
    QGridLayout
from PyQt6.QtCore import Qt

from controllers.SettingController import SettingController
from model.Settings import Settings


class SettingTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__controller = SettingController()
        self._init_ui()

        self.__controller.set_view(self)
        self.__controller.load_data()

    def _init_ui(self):
        # Create main container widget for shadow
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Title (outside shadow)
        title = QLabel("CẤU HÌNH BÃI XE VÀ GIÁ THẺ")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            font-size: 24px; 
            font-weight: bold; 
            color: #2e86c1;
            padding: 15px;
            background: transparent;
            """
        )
        container_layout.addWidget(title)

        # Content widget with shadow
        content_widget = QWidget()
        content_widget.setStyleSheet(
            """
            QWidget {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
            }
            """
        )
        content_widget.setGraphicsEffect(self.__create_shadow())

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # Button on top right
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.save_btn = QPushButton("Lưu cấu hình")
        self.save_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2e86c1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1f5f8b;
            }
            QPushButton:pressed {
                background-color: #174564;
            }
            """
        )
        self.save_btn.clicked.connect(self.__on_save_clicked)
        button_layout.addWidget(self.save_btn)
        content_layout.addLayout(button_layout)

        # Input fields styling
        input_style = """
            QLineEdit, QSpinBox {
                padding: 10px;
                font-size: 16px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                background-color: #f8f9fa;
                color: #2c3e50;
            }
            QLineEdit:focus, QSpinBox:focus {
                border: 2px solid #2e86c1;
                background-color: white;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border-radius: 3px;
            }
        """

        # Create grid layout
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # === GROUP 1: PRICING (Top Left - Highest Priority) ===
        group1 = QWidget()
        group1_layout = QVBoxLayout()
        group1_layout.setContentsMargins(15, 15, 15, 15)
        group1_layout.setSpacing(10)

        section_label = QLabel("CẤU HÌNH GIÁ")
        section_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495e;")
        group1_layout.addWidget(section_label)

        label = QLabel("Phí tháng (VND):")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        group1_layout.addWidget(label)
        self.monthly_fee_input = QLineEdit()
        self.monthly_fee_input.setStyleSheet(input_style)
        group1_layout.addWidget(self.monthly_fee_input)

        label = QLabel("Phí vé - Ban ngày (VND):")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        group1_layout.addWidget(label)
        self.single_day_input = QLineEdit()
        self.single_day_input.setStyleSheet(input_style)
        group1_layout.addWidget(self.single_day_input)

        label = QLabel("Phí vé - Ban đêm (VND):")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        group1_layout.addWidget(label)
        self.single_night_input = QLineEdit()
        self.single_night_input.setStyleSheet(input_style)
        group1_layout.addWidget(self.single_night_input)

        group1_layout.addStretch()
        group1.setLayout(group1_layout)
        group1.setStyleSheet("QWidget { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; }")

        # === GROUP 2: PARKING CAPACITY (Top Right) ===
        group2 = QWidget()
        group2_layout = QVBoxLayout()
        group2_layout.setContentsMargins(15, 15, 15, 15)
        group2_layout.setSpacing(10)

        section_label = QLabel("CẤU HÌNH BÃI XE")
        section_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495e;")
        group2_layout.addWidget(section_label)

        label = QLabel("Số lượng chỗ (slots):")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        group2_layout.addWidget(label)
        self.slots_spin = QSpinBox()
        self.slots_spin.setMinimum(0)
        self.slots_spin.setMaximum(100000)
        self.slots_spin.setStyleSheet(input_style)
        group2_layout.addWidget(self.slots_spin)

        group2_layout.addStretch()
        group2.setLayout(group2_layout)
        group2.setStyleSheet("QWidget { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; }")

        # === GROUP 3: PARKING RULES (Bottom Left) ===
        group3 = QWidget()
        group3_layout = QVBoxLayout()
        group3_layout.setContentsMargins(15, 15, 15, 15)
        group3_layout.setSpacing(10)

        section_label = QLabel("QUY ĐỊNH ĐỖ XE")
        section_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495e;")
        group3_layout.addWidget(section_label)

        label = QLabel("Thời gian đỗ tối đa (giờ):")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        group3_layout.addWidget(label)
        self.max_parking_hours_spin = QSpinBox()
        self.max_parking_hours_spin.setMinimum(1)
        self.max_parking_hours_spin.setMaximum(168)
        self.max_parking_hours_spin.setStyleSheet(input_style)
        group3_layout.addWidget(self.max_parking_hours_spin)

        label = QLabel("Phạt quá giờ (%):")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        group3_layout.addWidget(label)
        self.overtime_fee_spin = QSpinBox()
        self.overtime_fee_spin.setMinimum(0)
        self.overtime_fee_spin.setMaximum(200)
        self.overtime_fee_spin.setSuffix("%")
        self.overtime_fee_spin.setStyleSheet(input_style)
        group3_layout.addWidget(self.overtime_fee_spin)

        group3_layout.addStretch()
        group3.setLayout(group3_layout)
        group3.setStyleSheet("QWidget { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; }")

        # === GROUP 4: SYSTEM SETTINGS (Bottom Right) ===
        group4 = QWidget()
        group4_layout = QVBoxLayout()
        group4_layout.setContentsMargins(15, 15, 15, 15)
        group4_layout.setSpacing(10)

        section_label = QLabel(" CẤU HÌNH HỆ THỐNG")
        section_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495e;")
        group4_layout.addWidget(section_label)

        label = QLabel("Tốc độ làm mới camera (ms):")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        group4_layout.addWidget(label)
        self.camera_refresh_rate_spin = QSpinBox()
        self.camera_refresh_rate_spin.setMinimum(1)
        self.camera_refresh_rate_spin.setMaximum(200)
        self.camera_refresh_rate_spin.setSuffix(" ms")
        self.camera_refresh_rate_spin.setStyleSheet(input_style)
        group4_layout.addWidget(self.camera_refresh_rate_spin)

        label = QLabel("Thời gian xóa cache AI (giây):")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        group4_layout.addWidget(label)
        self.ai_cleanup_time_spin = QSpinBox()
        self.ai_cleanup_time_spin.setMinimum(1)
        self.ai_cleanup_time_spin.setMaximum(3600)
        self.ai_cleanup_time_spin.setSuffix(" giây")
        self.ai_cleanup_time_spin.setStyleSheet(input_style)
        group4_layout.addWidget(self.ai_cleanup_time_spin)

        group4.setLayout(group4_layout)
        group4.setStyleSheet("QWidget { background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; }")

        # Add groups to grid
        grid_layout.addWidget(group1, 0, 0)  # Top left
        grid_layout.addWidget(group2, 0, 1)  # Top right
        grid_layout.addWidget(group3, 1, 0)  # Bottom left
        grid_layout.addWidget(group4, 1, 1)  # Bottom right

        content_layout.addLayout(grid_layout)

        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        container_layout.addWidget(content_widget)

        container.setLayout(container_layout)

        # Set container as main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addWidget(container)
        self.setLayout(main_layout)

    def __create_shadow(self):
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        from PyQt6.QtGui import QColor

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        return shadow

    def set_data(self, settings: Settings):
        self.monthly_fee_input.setText(str(settings.monthly_fee))
        self.single_day_input.setText(str(settings.single_day_fee))
        self.single_night_input.setText(str(settings.single_night_fee))

        self.slots_spin.setValue(settings.total_slots)
        self.max_parking_hours_spin.setValue(settings.max_parking_hours)
        self.overtime_fee_spin.setValue(settings.overtime_fee)

        self.camera_refresh_rate_spin.setValue(settings.camera_refresh_rate)
        self.ai_cleanup_time_spin.setValue(settings.ai_cleanup_time)

    def __on_save_clicked(self):
        try:
            self.__controller.save_settings()
            QMessageBox.information(self, "Thành công", "Lưu cấu hình thành công.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lưu cấu hình thất bại: {e}")