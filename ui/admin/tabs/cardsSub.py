from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QFrame, QHeaderView, QCheckBox, QDialog, QDateEdit, QMessageBox,
    QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QDate
from datetime import datetime, timedelta


class SingleCardLogTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #F4F6F9;
                font-family: Segoe UI;
                font-size: 13px;
            }
            QLabel#Title {
                font-size: 22px;
                font-weight: 600;
                color: #1F2937;
            }
            QLineEdit {
                padding: 8px 10px;
                border-radius: 6px;
                border: 1px solid #D1D5DB;
                background: white;
            }
            QLineEdit:focus {
                border: 1px solid #2563EB;
            }
            QPushButton {
                padding: 8px 14px;
                border-radius: 6px;
                background-color: #E5E7EB;
            }
            QPushButton:hover {
                background-color: #D1D5DB;
            }
            QPushButton#Primary {
                background-color: #2563EB;
                color: white;
            }
            QPushButton#Primary:hover {
                background-color: #1D4ED8;
            }
            QPushButton#Danger {
                background-color: #DC2626;
                color: white;
            }
            QPushButton#Danger:hover {
                background-color: #B91C1C;
            }
            QTableWidget {
                background: white;
                border: none;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #F3F4F6;
                padding: 8px;
                border: none;
                font-weight: 600;
            }
            QTableWidget::item {
                padding: 6px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        # ===== Header =====
        lbl_title = QLabel("QUẢN LÝ LƯỢT GỬI XE – THẺ LƯỢT")
        lbl_title.setObjectName("Title")
        main_layout.addWidget(lbl_title)

        # ===== Search Card =====
        search_card = QFrame()
        search_card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 10px;
            }
        """)
        search_layout = QHBoxLayout(search_card)
        search_layout.setContentsMargins(16, 16, 16, 16)

        self.txtSearchCardCode = QLineEdit()
        self.txtSearchCardCode.setPlaceholderText("Nhập mã thẻ hoặc biển số...")

        self.btnSearch = QPushButton("Tìm kiếm")
        self.btnSearch.setObjectName("Primary")

        self.btnRefresh = QPushButton("Làm mới")

        search_layout.addWidget(self.txtSearchCardCode, 1)
        search_layout.addWidget(self.btnSearch)
        search_layout.addWidget(self.btnRefresh)

        main_layout.addWidget(search_card)

        # ===== Table =====
        self.tblCardLogs = QTableWidget()
        self.tblCardLogs.verticalHeader().setDefaultSectionSize(45)
        self.tblCardLogs.setColumnCount(10)
        self.tblCardLogs.setHorizontalHeaderLabels([
            "Mã thẻ", "Biển số", "Khách hàng",
            "Thời gian vào",
            "Thời gian ra",
            "Thời gian gửi", "Phí",
            "Trạng thái",
            "Nhân viên", "Ghi chú"
        ])
        self.tblCardLogs.horizontalHeader().setStretchLastSection(True)
        self.tblCardLogs.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tblCardLogs.setAlternatingRowColors(True)
        self.tblCardLogs.setShowGrid(False)
        self.tblCardLogs.verticalHeader().setVisible(False)

        main_layout.addWidget(self.tblCardLogs, 1)

        # ===== Action buttons =====
        action_layout = QHBoxLayout()
        action_layout.addStretch()

        self.btnAddLog = QPushButton("Xe vào bãi")
        self.btnAddLog.setObjectName("Primary")

        self.btnEditLog = QPushButton("Chỉnh sửa")
        self.btnDeleteLog = QPushButton("Xóa")
        self.btnDeleteLog.setObjectName("Danger")

        self.btnViewDetail = QPushButton("Chi tiết")

        action_layout.addWidget(self.btnAddLog)
        action_layout.addWidget(self.btnEditLog)
        action_layout.addWidget(self.btnDeleteLog)
        action_layout.addWidget(self.btnViewDetail)

        main_layout.addLayout(action_layout)


class MonthlyCardLogTab(QWidget):
    viewRequested = pyqtSignal(dict)
    editRequested = pyqtSignal(dict)
    deleteRequested = pyqtSignal(dict)
    cardAdded = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self._current_dialog = None
        self.init_ui()
        # self.populate_sample_data()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header Section - Simple
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

        lbl_title = QLabel("Quản lý thẻ tháng")
        lbl_title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #2c3e50;
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

        # Search and Add Button Row
        top_row = QHBoxLayout()
        top_row.setSpacing(15)

        # Search Box
        txtSearchCardCode = QLineEdit()
        txtSearchCardCode.setPlaceholderText("Tìm theo tên khách hàng...")

        search_action = QAction(QIcon("assets/icons/search.svg"), "", txtSearchCardCode)
        txtSearchCardCode.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)

        txtSearchCardCode.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)

        txtSearchCardCode.setMinimumWidth(350)
        txtSearchCardCode.setMaximumHeight(45)

        top_row.addWidget(txtSearchCardCode)
        top_row.addStretch()

        # Add Button
        btnAddCard = QPushButton("Thêm thẻ tháng")
        btnAddCard.setIcon(QIcon("assets/icons/plus.svg"))
        btnAddCard.setIconSize(QSize(16, 16))
        btnAddCard.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1;
                color: white;
                border: none;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #154360;
            }
            QPushButton:pressed {
                background-color: #0e3449;
            }
        """)
        btnAddCard.setMaximumHeight(45)
        btnAddCard.clicked.connect(self.show_add_card_dialog)
        top_row.addWidget(btnAddCard)

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

        self.tblCardLogs = QTableWidget()
        self.tblCardLogs.verticalHeader().setDefaultSectionSize(55)
        self.tblCardLogs.setColumnCount(9)
        self.tblCardLogs.setHorizontalHeaderLabels([
            "MÃ THẺ", "KHÁCH HÀNG", "BIỂN SỐ XE", "NGÀY BẮT ĐẦU",
            "NGÀY HẾT HẠN", "SỐ NGÀY", "PHÍ (VND)", "THANH TOÁN", "HÀNH ĐỘNG"
        ])

        # Enable sorting
        self.tblCardLogs.setSortingEnabled(True)

        self.tblCardLogs.setStyleSheet("""
            QTableWidget {
                background-color: white;
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
        header = self.tblCardLogs.horizontalHeader()

        for i in range(9):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        header.setSectionResizeMode(9, QHeaderView.ResizeMode.Fixed)  # Actions
        self.tblCardLogs.setColumnWidth(9, 180)

        self.tblCardLogs.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tblCardLogs.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tblCardLogs.setMinimumHeight(500)
        self.tblCardLogs.verticalHeader().setVisible(False)


        table_layout.addWidget(self.tblCardLogs)
        table_frame.setLayout(table_layout)
        content_layout.addWidget(table_frame)

        # Pagination info
        pagination_layout = QHBoxLayout()
        pagination_layout.setContentsMargins(0, 10, 0, 0)

        pagination_layout.addStretch()
        content_layout.addLayout(pagination_layout)

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

    def set_table_data(self, cards: list):
        self.tblCardLogs.setRowCount(0)  # Xóa dữ liệu cũ
        print(cards)
        print(len(cards))
        for card in cards:
            row = self.tblCardLogs.rowCount()
            self.tblCardLogs.insertRow(row)

            self.tblCardLogs.setItem(row, 0, QTableWidgetItem(card.card_code))
            self.tblCardLogs.setItem(row, 1, QTableWidgetItem(card.customer.fullname))
            self.tblCardLogs.setItem(row, 2, QTableWidgetItem(card.vehicle.plate_number))

            self.tblCardLogs.setItem(row, 3, QTableWidgetItem(card.start_date.strftime("%d/%m/%Y")))
            self.tblCardLogs.setItem(row, 4, QTableWidgetItem(card.expiry_date.strftime("%d/%m/%Y")))

            days = (card.expiry_date - card.start_date).days
            self.tblCardLogs.setItem(row, 5, QTableWidgetItem(str(days)))

            self.tblCardLogs.setItem(row, 6, QTableWidgetItem(f"{card.monthly_fee:,}"))

            paid_text = "Đã thanh toán" if card.is_paid else "Chưa thanh toán"
            self.tblCardLogs.setItem(row, 7, QTableWidgetItem(paid_text))

            action_widget = QWidget()
            layout = QHBoxLayout(action_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(2)


            btn_edit = QPushButton()
            btn_edit.setIcon(QIcon("assets/icons/edit.svg"))
            btn_edit.setIconSize(QSize(16, 16))
            btn_edit.setToolTip("Chỉnh sửa")

            btn_delete = QPushButton()
            btn_delete.setIcon(QIcon("assets/icons/delete.svg"))
            btn_delete.setIconSize(QSize(16, 16))
            btn_delete.setToolTip("Xóa")

            btn_delete.clicked.connect(lambda checked, c=card: self.on_delete_button_clicked(c))

            layout.addWidget(btn_edit)
            layout.addWidget(btn_delete)


            self.tblCardLogs.setCellWidget(row, 8, action_widget)

            # btn_edit.clicked.connect(lambda checked, c=card: self.edit_card(c))

    # add
    def show_add_card_dialog(self):

        if hasattr(self, "_current_dialog") and self._current_dialog is not None:
            self._current_dialog.raise_()
            self._current_dialog.activateWindow()
            return

        self._current_dialog = AddMonthlyCardDialog(self)
        # Gắn signal về tab
        self._current_dialog.cardAdded.connect(self.on_card_added)
        self._current_dialog.finished.connect(self._clear_dialog_reference)

        self._current_dialog.show()

    def _clear_dialog_reference(self):
        self._current_dialog = None

    def on_card_added(self, card_data: dict):
        print("Card data received:", card_data)
        self.cardAdded.emit(card_data)

    # delete
    def show_confirmation_dialog(self, title: str, message: str) -> bool:
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        # Tùy chỉnh nút
        yes_button = msg_box.button(QMessageBox.StandardButton.Yes)
        yes_button.setText("Xóa")
        no_button = msg_box.button(QMessageBox.StandardButton.No)
        no_button.setText("Hủy")

        # Chạy dialog
        result = msg_box.exec()  # exec() an toàn hơn exec_() trong PyQt6
        return result == QMessageBox.StandardButton.Yes

    def on_delete_button_clicked(self, card_data_object):

        data_to_delete = {
            'card_code': card_data_object.card_code,
        }

        self.deleteRequested.emit(data_to_delete)



class AddMonthlyCardDialog(QDialog):
    cardAdded = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm thẻ tháng mới")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("THÊM THẺ THÁNG MỚI")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2E86C1;
            padding-bottom: 10px;
        """)
        layout.addWidget(title)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("background-color: #e0e0e0;")
        layout.addWidget(divider)

        # Mã thẻ
        self.txtCardCode = self._create_form_row("Mã thẻ:", QLineEdit(), layout)
        self.txtCardCode.setPlaceholderText("Ví dụ: MC001")

        # Tên khách hàng
        self.txtCustomerName = self._create_form_row("Tên khách hàng:", QLineEdit(), layout)
        self.txtCustomerName.setPlaceholderText("Nhập tên đầy đủ")

        self.txtPhoneNumber = self._create_form_row("Số điện thoại:", QLineEdit(), layout)
        self.txtPhoneNumber.setPlaceholderText("Nhập số điện thoại")

        self.txtCustomerEmail = self._create_form_row("Email:", QLineEdit(), layout)
        self.txtCustomerEmail.setPlaceholderText("Ví dụ: tuan123@gmail.com")

        # Biển số xe
        self.txtPlateNumber = self._create_form_row("Biển số xe:", QLineEdit(), layout)
        self.txtPlateNumber.setPlaceholderText("Ví dụ: 30A-12345")

        # Loại xe
        self.cboVehicleType = self._create_form_row("Loại xe:", QComboBox(), layout)
        self.cboVehicleType.addItems(["Xe máy","Xe máy điện", "Xe đạp điện"])

        # Ngày bắt đầu
        self.dateStart = self._create_form_row("Ngày bắt đầu:", QDateEdit(), layout)
        self.dateStart.setDate(QDate.currentDate())
        self.dateStart.setCalendarPopup(True)
        self.dateStart.setDisplayFormat("dd/MM/yyyy")
        self.dateStart.dateChanged.connect(self.update_expiry_date)

        # Số tháng
        self.spinMonths = self._create_form_row("Số tháng:", QSpinBox(), layout)
        self.spinMonths.setMinimum(1)
        self.spinMonths.setMaximum(12)
        self.spinMonths.setValue(1)
        self.spinMonths.valueChanged.connect(self.update_expiry_date)

        # Ngày hết hạn (tự động tính)
        self.dateExpiry = self._create_form_row("Ngày hết hạn:", QDateEdit(), layout)
        self.dateExpiry.setDate(QDate.currentDate().addMonths(1))
        self.dateExpiry.setCalendarPopup(True)
        self.dateExpiry.setDisplayFormat("dd/MM/yyyy")
        self.dateExpiry.setReadOnly(True)

        # Phí tháng
        self.txtMonthlyFee = self._create_form_row("Phí tháng (VND):", QLineEdit(), layout)
        self.txtMonthlyFee.setPlaceholderText("Ví dụ: 200000")

        # Đã thanh toán
        self.chkIsPaid = QCheckBox("Đã thanh toán")
        self.chkIsPaid.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.chkIsPaid)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btnCancel = QPushButton("Hủy")
        btnCancel.setIcon(QIcon("assets/icons/close.svg"))
        btnCancel.clicked.connect(self.reject)
        btnCancel.setStyleSheet("""
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
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)

        btnSave = QPushButton("Lưu")
        btnSave.setIcon(QIcon("assets/icons/save.svg"))
        btnSave.clicked.connect(self.save_card)
        btnSave.setStyleSheet("""
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
            QPushButton:hover {
                background-color: #154360;
            }
        """)

        btn_layout.addWidget(btnCancel)
        btn_layout.addWidget(btnSave)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Styling
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit, QComboBox, QSpinBox, QDateEdit {
                padding: 8px;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus {
                border: 2px solid #2E86C1;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
            }
        """)

    def _create_form_row(self, label_text, widget, parent_layout):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)

        label = QLabel(label_text)
        label.setMinimumWidth(150)
        label.setStyleSheet("font-weight: 500;")

        row_layout.addWidget(label)
        row_layout.addWidget(widget, 1)

        parent_layout.addLayout(row_layout)
        return widget

    def update_expiry_date(self):
        start_date = self.dateStart.date()
        months = self.spinMonths.value()
        expiry_date = start_date.addMonths(months)
        self.dateExpiry.setDate(expiry_date)

    def save_card(self):
        # Validate
        if not self.txtCardCode.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mã thẻ!")
            return

        if not self.txtCustomerName.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên khách hàng!")
            return

        if not self.txtPhoneNumber.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số điện thoại khách hàng!")
            return

        if not self.txtPlateNumber.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập biển số xe!")
            return

        if not self.txtMonthlyFee.text().strip():
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập phí tháng!")
            return

        try:
            monthly_fee = int(self.txtMonthlyFee.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Phí tháng phải là số nguyên!")
            return

        # Tạo dictionary chứa dữ liệu
        card_data = {
            'card_code': self.txtCardCode.text().strip(),
            'customer_name': self.txtCustomerName.text().strip(),
            'phone_number': self.txtPhoneNumber.text().strip(),
            'customer_email': self.txtCustomerEmail.text().strip(),
            'plate_number': self.txtPlateNumber.text().strip(),
            'vehicle_type': self.cboVehicleType.currentText(),
            'start_date': self.dateStart.date().toPyDate(),
            'expiry_date': self.dateExpiry.date().toPyDate(),
            'months': self.spinMonths.value(),
            'monthly_fee': monthly_fee,
            'is_paid': self.chkIsPaid.isChecked()
        }

        # Emit signal
        self.cardAdded.emit(card_data)

        # Đóng dialog
        self.accept()