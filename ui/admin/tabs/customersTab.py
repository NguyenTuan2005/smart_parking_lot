from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog,
    QFrame, QAbstractItemView, QComboBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QAction
from dto.dtos import CustomerViewDTO
from typing import List


def create_status_widget(text, is_success):
    widget = QWidget()
    widget.setStyleSheet("background-color: transparent;")
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    label = QLabel(text)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    if is_success:
        bg_color = "#e8f5e9"  # green
        text_color = "#2A9B5A" 
        border_color = "#c8e6c9"
    else:
        bg_color = "#ffebee"  # red
        text_color = "#c62828"
        border_color = "#ffcdd2"

    label.setStyleSheet(f"""
        QLabel {{
            background-color: {bg_color};
            color: {text_color};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 4px 12px;
            font-weight: 600;
            font-size: 12px;
        }}
    """)
    layout.addWidget(label)
    return widget


class StatusItem(QTableWidgetItem):
    def __init__(self, text):
        super().__init__("")
        self.sort_key = text

    def __lt__(self, other):
        other_key = getattr(other, 'sort_key', other.text())
        return self.sort_key < other_key


class CustomerTab(QWidget):
    viewRequested = pyqtSignal(object)
    editRequested = pyqtSignal(object)
    lockRequested = pyqtSignal(object)
    unlockRequested = pyqtSignal(object)
    customerUpdated = pyqtSignal(object)
    refreshRequested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self._current_dialog = None
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header Section
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
                padding: 10px;
            }
        """)
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel("QUẢN LÝ KHÁCH HÀNG")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2e86c1;
        """)

        header_layout.addWidget(lbl_title)
        header_frame.setLayout(header_layout)
        main_layout.addWidget(header_frame)

        # Content Frame
        content_frame = QFrame()
        content_frame.setStyleSheet("background-color: #f8f9fa;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)

        # Search and Refresh Row
        top_row = QHBoxLayout()
        top_row.setSpacing(15)

        # Search Box
        self.txtSearch = QLineEdit()
        self.txtSearch.setPlaceholderText("Tìm theo tên, số điện thoại, biển số...")

        search_action = QAction(QIcon("assets/icons/search.svg"), "", self.txtSearch)
        self.txtSearch.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)

        self.txtSearch.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                padding-left: 10px;
                font-size: 14px;
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)

        self.txtSearch.setMinimumWidth(350)
        self.txtSearch.setMaximumHeight(45)

        # Search Button
        self.btnSearch = QPushButton("Tìm kiếm")
        self.btnSearch.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #154360; }
        """)

        # Refresh Button
        self.btnRefresh = QPushButton(" Làm mới")
        self.btnRefresh.setIcon(QIcon("assets/icons/refresh.png"))
        self.btnRefresh.setIconSize(QSize(15, 15))
        self.btnRefresh.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #dcdcdc;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        self.btnRefresh.clicked.connect(lambda: self.refreshRequested.emit())

        top_row.addWidget(self.txtSearch)
        top_row.addWidget(self.btnSearch)
        top_row.addWidget(self.btnRefresh)
        top_row.addStretch()

        # view locked customers
        self.btnNotify = QPushButton("Xem khách hàng bị khóa")
        self.btnNotify.setStyleSheet("""
            QPushButton {
                background-color: #2e86c1;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 6px;
            }
        """)
        self.btnNotify.setMaximumHeight(45)
        top_row.addWidget(self.btnNotify)


        content_layout.addLayout(top_row)

        # Table Section
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.table.verticalHeader().setDefaultSectionSize(55)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "TÊN KHÁCH HÀNG", "SỐ ĐIỆN THOẠI", "EMAIL", 
            "BIỂN SỐ XE", "LOẠI XE", "TRẠNG THÁI THẺ", "THÔNG BÁO HẾT HẠN", "HÀNH ĐỘNG"
        ])

        # Enable sorting
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #F2F7FF;
                border: none;
                gridline-color: #f0f0f0;
                selection-background-color: #e3f2fd;
            }
            QTableWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #f0f0f0;
                color: #2c3e50;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #2E86C1;
                color: white;
                padding: 14px 8px;
                border: none;
                font-weight: bold;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QHeaderView::section:hover {
                background-color: #154360;
            }
            QTableWidget::item:hover {
                background-color: #f8f9fa;
            }
            QTableCornerButton::section {
                background-color: #2E86C1;
                border: none;
            }
        """)

        # Set column widths
        header = self.table.horizontalHeader()
        for i in range(8):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)  # Actions
        self.table.setColumnWidth(7, 120)

        self.table.setMinimumHeight(500)
        self.table.verticalHeader().setVisible(False)

        table_layout.addWidget(self.table)
        table_frame.setLayout(table_layout)
        content_layout.addWidget(table_frame)

        content_frame.setLayout(content_layout)
        main_layout.addWidget(content_frame)

        # Set background
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        self.setLayout(main_layout)

    def set_table_data(self, customers: List[CustomerViewDTO], is_locked_view: bool = False):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        
        for customer in customers:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(customer.customer_name or ''))
            self.table.setItem(row, 1, QTableWidgetItem(customer.phone_number or ''))
            self.table.setItem(row, 2, QTableWidgetItem(customer.email or ''))
            self.table.setItem(row, 3, QTableWidgetItem(customer.plate_number or ''))
            self.table.setItem(row, 4, QTableWidgetItem(customer.vehicle_type or ''))

            # Card status column
            card_status = customer.card_status or 'Không xác định'
            item = StatusItem(card_status)
            self.table.setItem(row, 5, item)

            is_active = (card_status == "Còn hạn")
            status_widget = create_status_widget(card_status, is_active)
            self.table.setCellWidget(row, 5, status_widget)

            # Notification status column
            notified = customer.notified
            notified_text = "Đã gửi" if notified else "Chưa gửi"
            notified_item = StatusItem(notified_text)
            self.table.setItem(row, 6, notified_item)

            notified_widget = create_status_widget(notified_text, notified)
            self.table.setCellWidget(row, 6, notified_widget)

            # Action buttons
            action_widget = QWidget()
            action_widget.setStyleSheet("background-color: transparent;")
            layout = QHBoxLayout(action_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(20)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if not is_locked_view:
                btn_edit = QPushButton()
                btn_edit.setIcon(QIcon("assets/icons/edit.png"))
                btn_edit.setIconSize(QSize(16, 16))
                btn_edit.setToolTip("Chỉnh sửa")
                btn_edit.clicked.connect(lambda checked, c=customer: self.on_edit_clicked(c))

                btn_lock = QPushButton()
                btn_lock.setIcon(QIcon("assets/icons/lock.png"))
                btn_lock.setIconSize(QSize(16, 16))
                btn_lock.setToolTip("Khóa")
                btn_lock.clicked.connect(lambda checked, c=customer: self.on_lock_clicked(c))

                layout.addWidget(btn_edit)
                layout.addWidget(btn_lock)
            else:
                btn_unlock = QPushButton()
                btn_unlock.setIcon(QIcon("assets/icons/unlock.png"))
                btn_unlock.setIconSize(QSize(16, 16))
                btn_unlock.setToolTip("Mở khóa")
                btn_unlock.clicked.connect(lambda checked, c=customer: self.on_unlock_clicked(c))
                layout.addWidget(btn_unlock)

            self.table.setCellWidget(row, 7, action_widget)

        self.table.setSortingEnabled(True)

    def on_view_clicked(self, customer_dto: CustomerViewDTO):
        self.viewRequested.emit(customer_dto)

    def on_edit_clicked(self, customer_dto: CustomerViewDTO):
        self.show_edit_customer_dialog(customer_dto)

    def show_edit_customer_dialog(self, customer_dto: CustomerViewDTO):
        if self._current_dialog:
            self._current_dialog.raise_()
            self._current_dialog.activateWindow()
            return

        self._current_dialog = EditCustomerDialog(self, customer_dto)
        self._current_dialog.customerUpdated.connect(self.on_customer_updated)
        self._current_dialog.finished.connect(self._clear_dialog_reference)
        self._current_dialog.show()

    def on_customer_updated(self, customer_dto: CustomerViewDTO):
        self.customerUpdated.emit(customer_dto)

    def _clear_dialog_reference(self):
        self._current_dialog = None

    def on_lock_clicked(self, customer_dto: CustomerViewDTO):
        if self.show_confirmation_dialog(
            "Xác nhận khóa",
            f"Bạn có chắc chắn muốn khóa khách hàng '{customer_dto.customer_name}'?",
            "Khóa"
        ):
            self.lockRequested.emit(customer_dto)

    def on_unlock_clicked(self, customer_dto: CustomerViewDTO):
        if self.show_confirmation_dialog(
            "Xác nhận mở khóa",
            f"Bạn có chắc chắn muốn mở khóa cho khách hàng '{customer_dto.customer_name}'?",
            "Mở khóa"
        ):
            self.unlockRequested.emit(customer_dto)

    def show_confirmation_dialog(self, title: str, message: str, confirm_text: str = "Đồng ý") -> bool:
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
        yes_button.setText(confirm_text)
        no_button = msg_box.button(QMessageBox.StandardButton.No)
        no_button.setText("Hủy")

        result = msg_box.exec()
        return result == QMessageBox.StandardButton.Yes


class EditCustomerDialog(QDialog):
    customerUpdated = pyqtSignal(CustomerViewDTO)

    def __init__(self, parent=None, customer_dto=None):
        super().__init__(parent)
        self.setModal(True)
        self.setMinimumWidth(500)
        self._dto = customer_dto
        self.setWindowTitle("Chỉnh sửa thông tin khách hàng")
        self.init_ui()
        if customer_dto:
            self.load_customer_data(customer_dto)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel("CHỈNH SỬA THÔNG TIN KHÁCH HÀNG")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2E86C1;
            padding-bottom: 10px;
        """)
        layout.addWidget(self.title_label)

        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #e0e0e0; border: none;")
        layout.addWidget(divider)

        # Form
        self.txtCustomerName = self._create_form_row("Tên khách hàng:", QLineEdit(), layout)
        self.txtPhoneNumber = self._create_form_row("Số điện thoại:", QLineEdit(), layout)
        self.txtEmail = self._create_form_row("Email:", QLineEdit(), layout)
        self.txtPlateNumber = self._create_form_row("Biển số xe:", QLineEdit(), layout)
        self.cboVehicleType = self._create_form_row("Loại xe:", QComboBox(), layout)
        self.cboVehicleType.addItems(["Xe máy", "Xe máy điện", "Xe đạp điện"])

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btnCancel = QPushButton("Hủy")
        self.btnCancel.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 6px;
                min-width: 100px;
            }
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        self.btnCancel.clicked.connect(self.reject)

        self.btnSave = QPushButton("Lưu")
        self.btnSave.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1;
                color: white;
                border: none;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 6px;
                min-width: 100px;
            }
            QPushButton:hover { background-color: #154360; }
        """)
        self.btnSave.clicked.connect(self.save_customer)

        btn_layout.addWidget(self.btnCancel)
        btn_layout.addWidget(self.btnSave)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.setStyleSheet("""
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #2E86C1;
            }
            QLabel { font-size: 14px; }
        """)

    def _create_form_row(self, label_text, widget, parent_layout):
        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setMinimumWidth(150)
        row_layout.addWidget(label)
        row_layout.addWidget(widget, 1)
        parent_layout.addLayout(row_layout)
        return widget

    def load_customer_data(self, dto):
        self.txtCustomerName.setText(dto.customer_name or '')
        self.txtPhoneNumber.setText(dto.phone_number or '')
        self.txtEmail.setText(dto.email or '')
        self.txtPlateNumber.setText(dto.plate_number or '')
        idx = self.cboVehicleType.findText(dto.vehicle_type or 'Xe máy')
        if idx >= 0:
            self.cboVehicleType.setCurrentIndex(idx)

    def save_customer(self):
        # Validate
        if not self.txtCustomerName.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên khách hàng!")
            return
        if not self.txtPlateNumber.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập biển số xe!")
            return

        # Update DTO
        self._dto.customer_name = self.txtCustomerName.text().strip()
        self._dto.phone_number = self.txtPhoneNumber.text().strip()
        self._dto.email = self.txtEmail.text().strip()
        self._dto.plate_number = self.txtPlateNumber.text().strip()
        self._dto.vehicle_type = self.cboVehicleType.currentText()

        self.customerUpdated.emit(self._dto)
        self.accept()
