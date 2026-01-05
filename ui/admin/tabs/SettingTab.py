from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QHBoxLayout, QMessageBox
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
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Cấu hình bãi xe và giá thẻ")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(title)

        # Total slots
        self.slots_spin = QSpinBox()
        self.slots_spin.setMinimum(0)
        self.slots_spin.setMaximum(100000)
        layout.addWidget(QLabel("Số lượng chỗ (slots):"))
        layout.addWidget(self.slots_spin)

        # Monthly fee
        self.monthly_fee_input = QLineEdit()
        self.monthly_fee_input.setPlaceholderText("Số tiền (ví dụ 1500000)")
        layout.addWidget(QLabel("Phí tháng (VND):"))
        layout.addWidget(self.monthly_fee_input)

        # Day rate
        self.single_day_input = QLineEdit()
        self.single_day_input.setPlaceholderText("Phí ban ngày (VND)")
        layout.addWidget(QLabel("Phí vé - Ban ngày (VND):"))
        layout.addWidget(self.single_day_input)

        # Night rate
        self.single_night_input = QLineEdit()
        self.single_night_input.setPlaceholderText("Phí ban đêm (VND)")
        layout.addWidget(QLabel("Phí vé - Ban đêm (VND):"))
        layout.addWidget(self.single_night_input)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Lưu cấu hình")
        self.save_btn.clicked.connect(self.__on_save_clicked)
        btn_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton("Khôi phục mặc định")
        btn_layout.addWidget(self.reset_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def set_data(self, settings: Settings):
        self.slots_spin.setValue(settings.total_slots)
        self.monthly_fee_input.setText(str(settings.monthly_fee))
        self.single_day_input.setText(str(settings.single_day_fee))
        self.single_night_input.setText(str(settings.single_night_fee))

    def __on_save_clicked(self):
        try:
            self.__controller.save_settings()
            QMessageBox.information(self, "Thành công", "Lưu cấu hình thành công.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lưu cấu hình thất bại: {e}")


