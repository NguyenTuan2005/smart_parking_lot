from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
import json
from pathlib import Path
from datetime import datetime


class ParkingConfigTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)


        self._defaults = {
            "lot_name": "Parking Lot",
            "total_slots": 100,
            "monthly_fee": 1500000,
            "single_mode": "time_based",  # other possible: "flat"
            "day_start": 7,   # hour when 'day' starts (0-23)
            "day_end": 18,    # hour when 'day' ends (inclusive)
            "single_day_rate": 3000,
            "single_night_rate": 7000
        }

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        title = QLabel("Cấu hình bãi xe và giá thẻ")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 8px;")
        layout.addWidget(title)

        # Lot name
        self.lot_name_input = QLineEdit()
        self.lot_name_input.setPlaceholderText("Tên bãi xe")
        layout.addWidget(QLabel("Tên bãi xe:"))
        layout.addWidget(self.lot_name_input)

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

        # Single ticket (vé thường) configuration - motorbike only, day/night rates
        layout.addWidget(QLabel("--- Cấu hình vé thường (Xe máy) theo Ngày/Đêm ---"))

        # Day start/end (hours)
        hours_layout = QHBoxLayout()
        hours_layout.addWidget(QLabel("Bắt đầu Ngày (giờ 0-23):"))
        self.day_start_spin = QSpinBox()
        self.day_start_spin.setRange(0, 23)
        hours_layout.addWidget(self.day_start_spin)

        hours_layout.addWidget(QLabel("Kết thúc Ngày (giờ 0-23):"))
        self.day_end_spin = QSpinBox()
        self.day_end_spin.setRange(0, 23)
        hours_layout.addWidget(self.day_end_spin)

        layout.addLayout(hours_layout)

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
        btn_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton("Khôi phục mặc định")
        btn_layout.addWidget(self.reset_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)




