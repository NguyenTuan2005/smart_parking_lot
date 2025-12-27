from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt

# ===== STYLE =====
BTN_BLUE = """
QPushButton {
    background-color: #3498DB;
    color: white;
    border-radius: 6px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #2980B9;
}
"""

SEARCH_BAR_STYLE = """
QLineEdit {
    height: 30px;
    font-size: 13px;
    padding: 4px 10px;
    border: 1px solid #3498DB;
    border-radius: 6px;
}

QLineEdit:focus {
    border: 1px solid #2980B9;
}

QPushButton {
    height: 30px;
    min-width: 85px;
    font-size: 13px;
    color: white;
    background-color: #3498DB;
    border-radius: 6px;
}

QPushButton:hover {
    background-color: #2980B9;
}
"""


class VehicleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ===== MAIN LAYOUT =====
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        # ===== TITLE =====
        title = QLabel("QUẢN LÝ NHÂN VIÊN")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:#2E86C1;
        """)
        main_layout.addWidget(title)

        # ===== SEARCH BAR =====
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo tên nhân viên...")
        self.search_input.setStyleSheet(SEARCH_BAR_STYLE)

        self.search_btn = QPushButton("Tìm kiếm")
        self.search_btn.setStyleSheet(SEARCH_BAR_STYLE)

        self.refresh_btn = QPushButton("Làm mới")
        self.refresh_btn.setStyleSheet(SEARCH_BAR_STYLE)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(search_layout)

        # ===== TABLE =====
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Tên đầy đủ",
            "Số điện thoại",
            "Username",
            "Vai trò"
        ])

        # Ẩn cột ID
        self.table.setColumnHidden(0, True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        main_layout.addWidget(self.table, stretch=1)

        # ===== BUTTON BAR =====
        button_layout = QHBoxLayout()

        self.btn_add = QPushButton("Thêm nhân viên")
        self.btn_edit = QPushButton("Chỉnh sửa")
        self.btn_delete = QPushButton("Xóa nhân viên")
        self.btn_detail = QPushButton("Xem chi tiết")

        for btn in [
            self.btn_add,
            self.btn_edit,
            self.btn_delete,
            self.btn_detail
        ]:
            btn.setStyleSheet(BTN_BLUE)
            btn.setFixedHeight(40)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

    def set_table_data(self, rows):
        self.table.setRowCount(len(rows))

        for r, row in enumerate(rows):
            # row[0] = id
            self.table.setItem(r, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(r, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(r, 2, QTableWidgetItem(str(row[2])))
            self.table.setItem(r, 3, QTableWidgetItem(str(row[3])))

            role_text = "Admin" if row[5] == 1 else "Nhân viên"
            self.table.setItem(r, 4, QTableWidgetItem(role_text))

