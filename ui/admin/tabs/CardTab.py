from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtGui import QIcon, QAction, QColor
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QHeaderView,
    QCheckBox,
    QDialog,
    QDateEdit,
    QMessageBox,
    QComboBox,
    QSpinBox,
    QAbstractItemView,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QDate
from dto.dtos import MonthlyCardCreationDTO, CustomerDTO, VehicleDTO
from util.Validator import Validator


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

    label.setStyleSheet(
        f"""
        QLabel {{
            background-color: {bg_color};
            color: {text_color};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 4px 12px;
            font-weight: 600;
            font-size: 12px;
        }}
    """
    )
    layout.addWidget(label)
    return widget


class StatusItem(QTableWidgetItem):
    def __init__(self, text):
        super().__init__("")
        self.sort_key = text

    def __lt__(self, other):
        other_key = getattr(other, "sort_key", other.text())
        return self.sort_key < other_key


class CardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.card_tabs = QTabWidget()

        self.single_card_tab = SingleCardLogTab()
        self.single_card_management_tab = SingleCardManagementTab()
        self.monthly_card_tab = MonthlyCardLogTab()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.card_tabs.addTab(self.single_card_tab, "Nhật ký thẻ lượt")
        self.card_tabs.addTab(self.single_card_management_tab, "Thẻ lượt")
        self.card_tabs.addTab(self.monthly_card_tab, "Thẻ tháng")

        layout.addWidget(self.card_tabs)
        self.setLayout(layout)


class SingleCardLogTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """
        )

        header_frame = QFrame()
        header_frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
                padding: 10px;
            }
        """
        )
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel("QUẢN LÝ LƯỢT GỬI XE")
        lbl_title.setObjectName("Title")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet(
            """
            font-size: 24px; 
            font-weight: bold; 
            color: #2e86c1;
        """
        )
        header_layout.addWidget(lbl_title)

        main_layout.addWidget(header_frame)

        # Content Section
        content_frame = QFrame()
        content_frame.setStyleSheet("background-color: #f8f9fa;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        top_row = QHBoxLayout()
        top_row.setSpacing(15)

        # Search Bar
        self.txtSearchCardCode = QLineEdit()
        self.txtSearchCardCode.setPlaceholderText("Nhập mã thẻ hoặc biển số...")
        search_action = QAction(
            QIcon("assets/icons/search.svg"), "", self.txtSearchCardCode
        )
        self.txtSearchCardCode.addAction(
            search_action, QLineEdit.ActionPosition.LeadingPosition
        )

        self.txtSearchCardCode.setStyleSheet(
            """
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
        """
        )
        self.txtSearchCardCode.setMinimumWidth(350)
        self.txtSearchCardCode.setMaximumHeight(45)

        # Search Button
        self.btnSearch = QPushButton("Tìm kiếm")
        self.btnSearch.setStyleSheet(
            """
            QPushButton {
                background-color: #2E86C1;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #154360; }
        """
        )

        # Refresh Button
        self.btnRefresh = QPushButton(" Làm mới")
        self.btnRefresh.setIcon(QIcon("assets/icons/refresh.png"))
        self.btnRefresh.setIconSize(QSize(15, 15))
        self.btnRefresh.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #dcdcdc;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """
        )

        top_row.addWidget(self.txtSearchCardCode)
        top_row.addWidget(self.btnSearch)
        top_row.addWidget(self.btnRefresh)
        top_row.addStretch()

        content_layout.addLayout(top_row)

        # --- Table Section ---
        table_frame = QFrame()
        table_frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """
        )
        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.tblCardLogs = QTableWidget()
        self.tblCardLogs.verticalHeader().setDefaultSectionSize(55)
        self.tblCardLogs.setColumnCount(9)
        self.tblCardLogs.setSortingEnabled(True)
        self.tblCardLogs.setHorizontalHeaderLabels(
            [
                "MÃ THẺ",
                "BIỂN SỐ",
                "KHÁCH HÀNG",
                "THỜI GIAN VÀO",
                "THỜI GIAN RA",
                "THỜI GIAN GỬI",
                "PHÍ",
                "TRẠNG THÁI",
                "NHÂN VIÊN",
            ]
        )

        self.tblCardLogs.setStyleSheet(
            """
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
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QHeaderView::section:hover { background-color: #154360; }
        """
        )

        self.tblCardLogs.horizontalHeader().setStretchLastSection(True)
        self.tblCardLogs.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.tblCardLogs.setAlternatingRowColors(True)
        self.tblCardLogs.setShowGrid(False)
        self.tblCardLogs.verticalHeader().setVisible(False)
        self.tblCardLogs.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tblCardLogs.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tblCardLogs.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tblCardLogs.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        table_layout.addWidget(self.tblCardLogs)
        content_layout.addWidget(table_frame)

        main_layout.addWidget(content_frame)

    def set_table_data(self, logs: list):
        self.tblCardLogs.setSortingEnabled(False)
        self.tblCardLogs.setRowCount(0)
        for log in logs:
            row = self.tblCardLogs.rowCount()
            self.tblCardLogs.insertRow(row)

            self.tblCardLogs.setItem(
                row, 0, QTableWidgetItem(str(log.get("card_code") or ""))
            )
            self.tblCardLogs.setItem(
                row, 1, QTableWidgetItem(str(log.get("plate_number") or ""))
            )
            self.tblCardLogs.setItem(row, 2, QTableWidgetItem("Khách vãng lai"))

            entry_at = log.get("entry_at")
            entry_str = entry_at.strftime("%d/%m/%Y %H:%M") if entry_at else ""
            self.tblCardLogs.setItem(row, 3, QTableWidgetItem(entry_str))

            exit_at = log.get("exit_at")
            exit_str = exit_at.strftime("%d/%m/%Y %H:%M") if exit_at else ""
            self.tblCardLogs.setItem(row, 4, QTableWidgetItem(exit_str))

            # Duration
            duration_str = ""
            if entry_at:
                end_time = exit_at if exit_at else datetime.now()
                duration_minutes = int((end_time - entry_at).total_seconds() / 60)
                hours = duration_minutes // 60
                minutes = duration_minutes % 60
                duration_str = f"{hours}h {minutes}p"
            self.tblCardLogs.setItem(row, 5, QTableWidgetItem(duration_str))

            fee = log.get("fee", 0)
            self.tblCardLogs.setItem(row, 6, QTableWidgetItem(f"{fee:,}"))

            status = log.get("status", "") or ""
            item = StatusItem(status)
            self.tblCardLogs.setItem(row, 7, item)

            # Status styling with widget
            is_success_status = status == "Đã rời đi"
            status_widget = create_status_widget(status, is_success_status)
            self.tblCardLogs.setCellWidget(row, 7, status_widget)

            self.tblCardLogs.setItem(
                row, 8, QTableWidgetItem(str(log.get("staff_name") or ""))
            )

        self.tblCardLogs.setSortingEnabled(True)


class MonthlyCardLogTab(QWidget):
    viewRequested = pyqtSignal(dict)
    editRequested = pyqtSignal(MonthlyCardCreationDTO)
    deleteRequested = pyqtSignal(dict)
    cardAdded = pyqtSignal(MonthlyCardCreationDTO)
    addCardRequested = pyqtSignal()
    regenCodeRequested = pyqtSignal(object)

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
        header_frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
                padding: 10px;
            }
        """
        )
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        lbl_title = QLabel("QUẢN LÝ THẺ THÁNG")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet(
            """
            font-size: 24px; 
            font-weight: bold; 
            color: #2e86c1;
        """
        )

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
        self.txtSearchCardCode = QLineEdit()
        self.txtSearchCardCode.setPlaceholderText("Tìm theo tên, mã thẻ, biển số...")

        search_action = QAction(
            QIcon("assets/icons/search.svg"), "", self.txtSearchCardCode
        )
        self.txtSearchCardCode.addAction(
            search_action, QLineEdit.ActionPosition.LeadingPosition
        )

        self.txtSearchCardCode.setStyleSheet(
            """
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
        """
        )

        self.txtSearchCardCode.setMinimumWidth(350)
        self.txtSearchCardCode.setMaximumHeight(45)

        # Search Button
        self.btnSearch = QPushButton("Tìm kiếm")
        self.btnSearch.setStyleSheet(
            """
            QPushButton {
                 background-color: #2E86C1;
                 color: white;
                 border: none;
                 padding: 10px 20px;
                 border-radius: 6px;
                 font-weight: 600;
             }
             QPushButton:hover { background-color: #154360; }
        """
        )

        # Refresh Button
        self.btnRefresh = QPushButton(" Làm mới")
        self.btnRefresh.setIcon(QIcon("assets/icons/refresh.png"))
        self.btnRefresh.setIconSize(QSize(15, 15))
        self.btnRefresh.setStyleSheet(
            """
             QPushButton {
                 background-color: #ffffff;
                 color: #333;
                 border: 1px solid #dcdcdc;
                 padding: 10px 20px;
                 border-radius: 6px;
                 font-weight: 600;
             }
             QPushButton:hover { background-color: #f0f0f0; }
        """
        )

        top_row.addWidget(self.txtSearchCardCode)
        top_row.addWidget(self.btnSearch)
        top_row.addWidget(self.btnRefresh)
        top_row.addStretch()

        # Add Button
        self.btnAddCard = QPushButton(" Thêm thẻ tháng")
        self.btnAddCard.setIcon(QIcon("assets/icons/add.png"))
        self.btnAddCard.setIconSize(QSize(30, 30))
        self.btnAddCard.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
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
        """
        )
        self.btnAddCard.setMaximumHeight(40)
        self.btnAddCard.clicked.connect(self.on_add_card_clicked)
        top_row.addWidget(self.btnAddCard)

        content_layout.addLayout(top_row)

        # Table Section
        table_frame = QFrame()
        table_frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """
        )
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(0, 0, 0, 0)
        table_layout.setSpacing(0)

        self.tblCardLogs = QTableWidget()
        self.tblCardLogs.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.tblCardLogs.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.tblCardLogs.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.tblCardLogs.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.tblCardLogs.verticalHeader().setDefaultSectionSize(55)
        self.tblCardLogs.setColumnCount(9)
        self.tblCardLogs.setHorizontalHeaderLabels(
            [
                "MÃ THẺ",
                "KHÁCH HÀNG",
                "BIỂN SỐ XE",
                "NGÀY BẮT ĐẦU",
                "NGÀY HẾT HẠN",
                "SỐ NGÀY",
                "PHÍ (VND)",
                "THANH TOÁN",
                "HÀNH ĐỘNG",
            ]
        )

        # Enable sorting
        self.tblCardLogs.setSortingEnabled(True)
        self.tblCardLogs.setAlternatingRowColors(True)

        self.tblCardLogs.setStyleSheet(
            """
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
        """
        )

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
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """
        )

        self.setLayout(main_layout)

    def set_table_data(self, cards: list):
        self.tblCardLogs.setSortingEnabled(False)
        self.tblCardLogs.setRowCount(0)  # Xóa dữ liệu cũ
        for card in cards:
            row = self.tblCardLogs.rowCount()
            self.tblCardLogs.insertRow(row)

            self.tblCardLogs.setItem(row, 0, QTableWidgetItem(card.card_code))
            self.tblCardLogs.setItem(row, 1, QTableWidgetItem(card.customer.fullname))
            self.tblCardLogs.setItem(
                row, 2, QTableWidgetItem(card.vehicle.plate_number)
            )

            self.tblCardLogs.setItem(
                row, 3, QTableWidgetItem(card.start_date.strftime("%d/%m/%Y"))
            )
            self.tblCardLogs.setItem(
                row, 4, QTableWidgetItem(card.expiry_date.strftime("%d/%m/%Y"))
            )

            days = (card.expiry_date - card.start_date).days
            self.tblCardLogs.setItem(row, 5, QTableWidgetItem(str(days)))

            self.tblCardLogs.setItem(row, 6, QTableWidgetItem(f"{card.monthly_fee:,}"))

            paid_text = "Đã thanh toán" if card.is_paid else "Chưa thanh toán"
            item = StatusItem(paid_text)
            self.tblCardLogs.setItem(row, 7, item)

            is_paid_success = card.is_paid
            status_widget = create_status_widget(paid_text, is_paid_success)
            self.tblCardLogs.setCellWidget(row, 7, status_widget)

            action_widget = QWidget()
            action_widget.setStyleSheet("background-color: transparent;")
            layout = QHBoxLayout(action_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(20)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            btn_edit = QPushButton()
            btn_edit.setIcon(QIcon("assets/icons/edit.png"))
            btn_edit.setIconSize(QSize(16, 16))
            btn_edit.setToolTip("Chỉnh sửa")

            btn_delete = QPushButton()
            btn_delete.setIcon(QIcon("assets/icons/delete.svg"))
            btn_delete.setIconSize(QSize(16, 16))
            btn_delete.setToolTip("Xóa")

            btn_delete.clicked.connect(
                lambda checked, c=card: self.on_delete_button_clicked(c)
            )

            try:
                # set_table_data
                btn_edit.clicked.connect(
                    lambda checked, c=card: self.show_edit_card_dialog(
                        {
                            "card_id": c.card_id,
                            "customer_id": c.customer.id,
                            "vehicle_id": c.vehicle.vehicle_id,
                            "card_code": c.card_code,
                            "customer_name": c.customer.fullname,
                            "phone_number": getattr(c.customer, "phone_number", ""),
                            "customer_email": getattr(c.customer, "email", ""),
                            "plate_number": c.vehicle.plate_number,
                            "vehicle_type": getattr(c.vehicle, "type", "Xe máy"),
                            "start_date": c.start_date,
                            "expiry_date": c.expiry_date,
                            "months": (c.expiry_date - c.start_date).days // 30,
                            "monthly_fee": c.monthly_fee,
                            "is_paid": c.is_paid,
                        }
                    )
                )
            except Exception as e:
                print(f"Error accessing card data: {e}")

            layout.addWidget(btn_edit)
            layout.addWidget(btn_delete)

            self.tblCardLogs.setCellWidget(row, 8, action_widget)

        self.tblCardLogs.setSortingEnabled(True)

    def on_add_card_clicked(self):
        self.addCardRequested.emit()

    # add
    def show_add_card_dialog(self, card_data=None, next_code=None):
        if self._current_dialog:
            self._current_dialog.raise_()
            self._current_dialog.activateWindow()
            return
        self._current_dialog = AddMonthlyCardDialog(
            self, card_data=card_data, next_code=next_code
        )
        if card_data is None:
            self._current_dialog.cardAdded.connect(self.on_card_added)
            self._current_dialog.regenCodeRequested.connect(
                lambda: self.regenCodeRequested.emit(self._current_dialog)
            )
        else:
            self._current_dialog.cardUpdated.connect(self.on_card_updated)
        self._current_dialog.finished.connect(self._clear_dialog_reference)
        self._current_dialog.show()

    def on_card_added(self, card_data):
        # Thêm một dòng mới
        row = self.tblCardLogs.rowCount()
        self.tblCardLogs.insertRow(row)

        # Điền dữ liệu vào các cột
        self.tblCardLogs.setItem(row, 0, QTableWidgetItem(card_data.card_code))
        self.tblCardLogs.setItem(row, 1, QTableWidgetItem(card_data.customer.fullname))
        self.tblCardLogs.setItem(
            row, 2, QTableWidgetItem(card_data.vehicle.plate_number)
        )
        self.tblCardLogs.setItem(
            row, 3, QTableWidgetItem(card_data.start_date.strftime("%d/%m/%Y"))
        )
        self.tblCardLogs.setItem(
            row, 4, QTableWidgetItem(card_data.expiry_date.strftime("%d/%m/%Y"))
        )
        self.tblCardLogs.setItem(row, 5, QTableWidgetItem(str(card_data.months)))
        self.tblCardLogs.setItem(row, 6, QTableWidgetItem(f"{card_data.monthly_fee:,}"))
        paid_text = "Đã thanh toán" if card_data.is_paid else "Chưa thanh toán"
        item = StatusItem(paid_text)
        self.tblCardLogs.setItem(row, 7, item)

        is_paid_success = card_data.is_paid
        status_widget = create_status_widget(paid_text, is_paid_success)
        self.tblCardLogs.setCellWidget(row, 7, status_widget)

        # Tạo cell chứa các nút hành động (edit/delete)
        action_widget = QWidget()
        action_widget.setStyleSheet("background-color: transparent;")
        layout = QHBoxLayout(action_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_edit = QPushButton()
        btn_edit.setIcon(QIcon("assets/icons/edit.png"))
        btn_edit.setIconSize(QSize(16, 16))
        btn_edit.setToolTip("Chỉnh sửa")
        btn_edit.clicked.connect(lambda _, c=card_data: self.show_edit_card_dialog(c))

        btn_delete = QPushButton()
        btn_delete.setIcon(QIcon("assets/icons/delete.svg"))
        btn_delete.setIconSize(QSize(16, 16))
        btn_delete.setToolTip("Xóa")
        btn_delete.clicked.connect(
            lambda _, c=card_data: self.on_delete_button_clicked(c)
        )

        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)

        self.tblCardLogs.setCellWidget(row, 8, action_widget)

        self.cardAdded.emit(card_data)

    # Sửa
    def show_edit_card_dialog(self, card_data):
        if self._current_dialog:
            self._current_dialog.raise_()
            self._current_dialog.activateWindow()
            return
        self._current_dialog = AddMonthlyCardDialog(self, card_data)
        self._current_dialog.cardUpdated.connect(self.on_card_updated)
        self._current_dialog.finished.connect(self._clear_dialog_reference)
        self._current_dialog.show()

    def on_card_updated(self, card_data: MonthlyCardCreationDTO):
        self.editRequested.emit(card_data)

    # delete
    def show_confirmation_dialog(self, title: str, message: str) -> bool:
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
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
            "card_code": card_data_object.card_code,
        }

        self.deleteRequested.emit(data_to_delete)

    def _clear_dialog_reference(self):
        self._current_dialog = None


class AddMonthlyCardDialog(QDialog):
    cardAdded = pyqtSignal(MonthlyCardCreationDTO)
    cardUpdated = pyqtSignal(MonthlyCardCreationDTO)
    regenCodeRequested = pyqtSignal()

    def __init__(self, parent=None, card_data=None, next_code=None):
        super().__init__(parent)
        self.btnCancel = None
        self.btnSave = None
        self.setModal(True)
        self.setMinimumWidth(600)
        self._editing_card = card_data
        self._next_code = next_code
        self.setWindowTitle(
            "Chỉnh sửa thẻ tháng" if card_data else "Thêm thẻ tháng mới"
        )
        self.init_ui()
        if card_data:
            self.load_card_data(card_data)
        elif next_code:
            self.txtCardCode.setText(next_code)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(
            """
                font-size: 20px;
                font-weight: bold;
                color: #2E86C1;
                padding-bottom: 10px;
            """
        )
        layout.addWidget(self.title_label)

        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #e0e0e0; border: none;")
        layout.addWidget(divider)

        # form
        # Card Code with Regen Button
        code_row = QHBoxLayout()
        code_label = QLabel("Mã thẻ:")
        code_label.setMinimumWidth(150)
        code_row.addWidget(code_label)

        self.txtCardCode = QLineEdit()
        self.txtCardCode.setPlaceholderText("Nhập hoặc tạo mã tự động...")
        code_row.addWidget(self.txtCardCode, 1)

        self.btnRegenCode = QPushButton()
        self.btnRegenCode.setIcon(QIcon("assets/icons/refresh.png"))
        self.btnRegenCode.setIconSize(QSize(20, 20))
        self.btnRegenCode.setToolTip("Tạo mã tự động")
        self.btnRegenCode.setFixedSize(40, 40)
        self.btnRegenCode.setStyleSheet(
            """
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dcdcdc;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #2E86C1;
            }
        """
        )
        self.btnRegenCode.clicked.connect(self.regenCodeRequested.emit)
        code_row.addWidget(self.btnRegenCode)
        layout.addLayout(code_row)

        if self._editing_card:
            self.btnRegenCode.setVisible(False)
            self.txtCardCode.setReadOnly(True)
            self.txtCardCode.setStyleSheet("background-color: #f5f5f5; color: #7f8c8d;")

        self.txtCustomerName = self._create_form_row(
            "Tên khách hàng:", QLineEdit(), layout
        )
        self.txtPhoneNumber = self._create_form_row(
            "Số điện thoại:", QLineEdit(), layout
        )
        self.txtCustomerEmail = self._create_form_row("Email:", QLineEdit(), layout)
        self.txtPlateNumber = self._create_form_row("Biển số xe:", QLineEdit(), layout)
        self.cboVehicleType = self._create_form_row("Loại xe:", QComboBox(), layout)
        self.cboVehicleType.addItems(["Xe máy", "Xe máy điện", "Xe đạp điện"])
        self.dateStart = self._create_form_row("Ngày bắt đầu:", QDateEdit(), layout)
        self.dateStart.setCalendarPopup(True)
        self.dateStart.setDisplayFormat("dd/MM/yyyy")
        self.dateStart.setDate(QDate.currentDate())
        self.dateStart.dateChanged.connect(self.update_expiry_date)

        self.spinMonths = self._create_form_row("Số tháng:", QSpinBox(), layout)
        self.spinMonths.setMinimum(1)
        self.spinMonths.setMaximum(12)
        self.spinMonths.valueChanged.connect(self.update_expiry_date)

        self.dateExpiry = self._create_form_row("Ngày hết hạn:", QDateEdit(), layout)
        self.dateExpiry.setCalendarPopup(True)
        self.dateExpiry.setDisplayFormat("dd/MM/yyyy")
        self.dateExpiry.setReadOnly(True)

        self.txtMonthlyFee = self._create_form_row(
            "Phí tháng (VND):", QLineEdit(), layout
        )
        self.txtMonthlyFee.setReadOnly(True)
        self.txtMonthlyFee.setStyleSheet(
            self.txtMonthlyFee.styleSheet() + "background-color: #f5f5f5;"
        )

        chk_container = QWidget()
        chk_layout = QHBoxLayout(chk_container)
        chk_layout.setContentsMargins(0, 0, 0, 0)

        self.chkIsPaid = QCheckBox("Đã thanh toán")
        self.chkIsPaid.setCheckable(True)
        self.chkIsPaid.setChecked(False)
        self.chkIsPaid.setStyleSheet(
            """
            QCheckBox {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                background: white;
                margin-top: 1px;
            }
            QCheckBox::indicator:hover {
                border-color: #2E86C1;
                background-color: #f4f6f7;
            }
            QCheckBox::indicator:checked {
                background-color: #2E86C1;
                border-color: #2E86C1;
                image: url(assets/icons/checkbox-tick.png);
            }
            QCheckBox::indicator:checked:hover {
                background-color: #2573a7;
                border-color: #2573a7;
            }
        """
        )

        chk_layout.addWidget(self.chkIsPaid)
        chk_layout.addStretch()

        layout.addWidget(chk_container)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btnCancel = QPushButton("Hủy")
        self.btnCancel.setStyleSheet(
            """
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
               """
        )
        self.btnCancel.clicked.connect(self.reject)

        self.btnSave = QPushButton("Lưu")
        self.btnSave.setStyleSheet(
            """
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
              """
        )
        self.btnSave.clicked.connect(self.save_card)

        btn_layout.addWidget(self.btnCancel)
        btn_layout.addWidget(self.btnSave)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.update_expiry_date()
        self.setStyleSheet(
            """
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
 
                    }
                """
        )

        self.update_title()

    def update_title(self):
        if self._editing_card:
            self.title_label.setText("CHỈNH SỬA THẺ THÁNG")
        else:
            self.title_label.setText("THÊM THẺ THÁNG MỚI")

    def set_card_code(self, code):
        self.txtCardCode.setText(code)

    def load_card_data(self, card_data):
        """Điền dữ liệu vào dialog khi edit"""
        # Chặn tín hiệu để không tự tính lại ngày/phí khi đang load
        self.dateStart.blockSignals(True)
        self.spinMonths.blockSignals(True)

        self.txtCardCode.setText(card_data.get("card_code", ""))
        self.txtCustomerName.setText(card_data.get("customer_name", ""))
        self.txtPhoneNumber.setText(card_data.get("phone_number", ""))
        self.txtCustomerEmail.setText(card_data.get("customer_email", ""))
        self.txtPlateNumber.setText(card_data.get("plate_number", ""))

        vehicle_type = card_data.get("vehicle_type", "Xe máy")
        idx = self.cboVehicleType.findText(vehicle_type)
        if idx >= 0:
            self.cboVehicleType.setCurrentIndex(idx)

        start_date = card_data.get("start_date", QDate.currentDate().toPyDate())
        self.dateStart.setDate(QDate(start_date.year, start_date.month, start_date.day))

        months = card_data.get("months", 1)
        self.spinMonths.setValue(months)

        self.update_expiry_date()

        fee = card_data.get("monthly_fee", 0)
        self.txtMonthlyFee.setText(f"{fee:,}")

        self.chkIsPaid.setChecked(card_data.get("is_paid", False))

        self.dateStart.blockSignals(False)
        self.spinMonths.blockSignals(False)

    def _create_form_row(self, label_text, widget, parent_layout):
        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setMinimumWidth(150)
        row_layout.addWidget(label)
        row_layout.addWidget(widget, 1)
        parent_layout.addLayout(row_layout)
        return widget

    def update_expiry_date(self):
        start_date = self.dateStart.date()
        months = self.spinMonths.value()
        expiry_date = start_date.addMonths(months)
        self.dateExpiry.setDate(expiry_date)

        total_fee = months * 60000
        self.txtMonthlyFee.setText(f"{total_fee:,}")

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

        email = self.txtCustomerEmail.text().strip()
        if email and not Validator.is_valid_email(email):
            QMessageBox.warning(self, "Lỗi", "Định dạng email không hợp lệ!")
            return

        phone = self.txtPhoneNumber.text().strip()
        if not Validator.is_valid_phone(phone):
            QMessageBox.warning(
                self, "Lỗi", "Số điện thoại không hợp lệ (phải có 10 chữ số)!"
            )
            return

        try:
            fee_str = self.txtMonthlyFee.text().replace(",", "")
            fee = int(fee_str) if fee_str else 0
        except ValueError:
            fee = 0

        # Create DTO obj
        customer_dto = CustomerDTO(
            fullname=self.txtCustomerName.text().strip(),
            phone_number=self.txtPhoneNumber.text().strip(),
            email=self.txtCustomerEmail.text().strip(),
        )

        vehicle_dto = VehicleDTO(
            vehicle_type=self.cboVehicleType.currentText(),
            plate_number=self.txtPlateNumber.text().strip(),
        )

        card_dto = MonthlyCardCreationDTO(
            card_code=self.txtCardCode.text().strip(),
            customer=customer_dto,
            vehicle=vehicle_dto,
            monthly_fee=fee,
            start_date=self.dateStart.date().toPyDate(),
            expiry_date=self.dateExpiry.date().toPyDate(),
            is_paid=self.chkIsPaid.isChecked(),
            months=self.spinMonths.value(),
        )

        # Retrieve IDs if editing
        if self._editing_card:
            card_dto.card_id = self._editing_card.get("card_id")
            card_dto.customer_id = self._editing_card.get("customer_id")
            card_dto.vehicle_id = self._editing_card.get("vehicle_id")
            self.cardUpdated.emit(card_dto)
        else:
            self.cardAdded.emit(card_dto)

        self.accept()


class SingleCardManagementTab(QWidget):
    createRequested = pyqtSignal(dict)
    updateRequested = pyqtSignal(dict)
    deleteRequested = pyqtSignal(int)
    addCardRequested = pyqtSignal()
    regenCodeRequested = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet(
            "background-color: white; border-bottom: 1px solid #e0e0e0; padding: 5px;"
        )
        header_layout = QVBoxLayout(header_frame)
        lbl_title = QLabel("QUẢN LÝ THẺ LƯỢT")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: #2e86c1; text-align: center;"
        )
        header_layout.addWidget(lbl_title)
        main_layout.addWidget(header_frame)

        # Content
        content_frame = QFrame()
        content_frame.setStyleSheet("background-color: #f8f9fa;")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Top Controls
        top_row = QHBoxLayout()
        top_row.setSpacing(20)

        # Search Bar
        self.txtSearch = QLineEdit()
        self.txtSearch.setPlaceholderText("Tìm theo mã thẻ, giá vé...")

        search_action = QAction(QIcon("assets/icons/search.svg"), "", self.txtSearch)
        self.txtSearch.addAction(
            search_action, QLineEdit.ActionPosition.LeadingPosition
        )

        self.txtSearch.setStyleSheet(
            """
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
        """
        )
        self.txtSearch.setMinimumWidth(350)
        self.txtSearch.setMaximumHeight(45)

        # Search Button
        self.btnSearch = QPushButton("Tìm kiếm")
        self.btnSearch.setStyleSheet(
            """
            QPushButton {
                 background-color: #2E86C1;
                 color: white;
                 border: none;
                 padding: 10px 20px;
                 border-radius: 6px;
                 font-weight: 600;
             }
             QPushButton:hover { background-color: #154360; }
        """
        )

        # Refresh Button
        self.btnRefresh = QPushButton(" Làm mới")
        self.btnRefresh.setIcon(QIcon("assets/icons/refresh.png"))
        self.btnRefresh.setIconSize(QSize(15, 15))
        self.btnRefresh.setStyleSheet(
            """
             QPushButton {
                 background-color: #ffffff;
                 color: #333;
                 border: 1px solid #dcdcdc;
                 padding: 10px 20px;
                 border-radius: 6px;
                 font-weight: 600;
             }
             QPushButton:hover { background-color: #f0f0f0; }
        """
        )

        top_row.addWidget(self.txtSearch)
        top_row.addWidget(self.btnSearch)
        top_row.addWidget(self.btnRefresh)
        top_row.addStretch()

        # Add Button (moved to right)
        self.btnAdd = QPushButton(" Thêm thẻ lượt")
        self.btnAdd.setIcon(QIcon("assets/icons/add.png"))
        self.btnAdd.setIconSize(QSize(30, 30))
        self.btnAdd.setStyleSheet(
            """
            QPushButton {
                background-color: #27ae60;
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
        """
        )
        self.btnAdd.setMaximumHeight(40)
        self.btnAdd.clicked.connect(self.on_add_clicked)
        top_row.addWidget(self.btnAdd)

        content_layout.addLayout(top_row)

        # Table
        self.table = QTableWidget()
        self.table.verticalHeader().setDefaultSectionSize(55)
        self.table.setColumnCount(5)
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.setHorizontalHeaderLabels(
            ["MÃ THẺ", "GIÁ VÉ", "GIÁ VÉ ĐÊM", "TRẠNG THÁI", "HÀNH ĐỘNG"]
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 150)

        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(
            """
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
        """
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        content_layout.addWidget(self.table)

        main_layout.addWidget(content_frame)

    def set_table_data(self, cards):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for card in cards:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(card.card_code or "")))

            price = card.price if card.price is not None else 0
            self.table.setItem(row, 1, QTableWidgetItem(f"{price:,}"))

            night_price = card.night_price if card.night_price is not None else 0
            self.table.setItem(row, 2, QTableWidgetItem(f"{night_price:,}"))

            self.table.setItem(row, 3, QTableWidgetItem("Hoạt động"))

            container = QWidget()
            container.setStyleSheet("background-color: transparent;")
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(20)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            btn_edit = QPushButton()
            btn_edit.setIcon(QIcon("assets/icons/edit.png"))
            btn_edit.setIconSize(QSize(16, 16))
            btn_edit.setToolTip("Chỉnh sửa")
            btn_edit.clicked.connect(lambda _, c=card: self.show_edit_dialog(c))

            btn_delete = QPushButton()
            btn_delete.setIcon(QIcon("assets/icons/delete.svg"))
            btn_delete.setIconSize(QSize(16, 16))
            btn_delete.setToolTip("Xóa")
            btn_delete.clicked.connect(
                lambda _, c_id=card.card_id: self.on_delete_clicked(c_id)
            )

            layout.addWidget(btn_edit)
            layout.addWidget(btn_delete)
            self.table.setCellWidget(row, 4, container)

        self.table.setSortingEnabled(True)

    def on_delete_clicked(self, card_id):
        reply = QMessageBox.question(
            self,
            "Xác nhận xóa",
            "Bạn có chắc chắn muốn xóa thẻ này không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.deleteRequested.emit(card_id)

    def on_add_clicked(self):
        self.addCardRequested.emit()

    def show_add_dialog(self, next_code=None):
        dlg = SingleCardDialog(self, next_code=next_code)
        dlg.regenCodeRequested.connect(lambda: self.regenCodeRequested.emit(dlg))
        if dlg.exec():
            self.createRequested.emit(dlg.get_data())

    def show_edit_dialog(self, card):
        dlg = SingleCardDialog(self, card)
        if dlg.exec():
            data = dlg.get_data()
            data["card_id"] = card.card_id
            self.updateRequested.emit(data)


class SingleCardDialog(QDialog):
    regenCodeRequested = pyqtSignal()

    def __init__(self, parent=None, card=None, next_code=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm thẻ lượt" if not card else "Sửa thẻ lượt")
        self.setMinimumWidth(500)
        self._card = card
        self._next_code = next_code
        self.init_ui()
        if not card and next_code:
            self.txtCode.setText(next_code)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel("THÊM THẺ LƯỢT" if not self._card else "SỬA THẺ LƯỢT")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #2E86C1; padding-bottom: 10px;"
        )
        layout.addWidget(title_label)

        # Divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background-color: #e0e0e0; border: none;")
        layout.addWidget(divider)

        # Form
        # Code row with regen button
        code_row_layout = QHBoxLayout()
        code_label = QLabel("Mã thẻ:")
        code_label.setMinimumWidth(150)
        code_row_layout.addWidget(code_label)

        self.txtCode = QLineEdit()
        self.txtCode.setPlaceholderText("Nhập hoặc tạo mã tự động...")
        code_row_layout.addWidget(self.txtCode, 1)

        self.btnRegenCode = QPushButton()
        self.btnRegenCode.setIcon(QIcon("assets/icons/refresh.png"))
        self.btnRegenCode.setIconSize(QSize(20, 20))
        self.btnRegenCode.setToolTip("Tạo mã tự động")
        self.btnRegenCode.setFixedSize(40, 40)
        self.btnRegenCode.setStyleSheet(
            """
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #dcdcdc;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #2E86C1;
            }
        """
        )
        self.btnRegenCode.clicked.connect(self.regenCodeRequested.emit)
        code_row_layout.addWidget(self.btnRegenCode)
        layout.addLayout(code_row_layout)

        if self._card:
            self.btnRegenCode.setVisible(False)
            self.txtCode.setReadOnly(True)
            self.txtCode.setStyleSheet("background-color: #f5f5f5; color: #7f8c8d;")

        self.txtPrice = self._create_form_row("Giá vé (VND):", QLineEdit(), layout)
        self.txtPrice.setPlaceholderText("Nhập giá vé")

        if self._card:
            self.txtCode.setText(self._card.card_code)
            self.txtCode.setReadOnly(True)
            self.txtPrice.setText(str(self._card.price))

        self.txtNightPrice = self._create_form_row(
            "Giá vé đêm (VND):", QLineEdit(), layout
        )
        self.txtNightPrice.setPlaceholderText("Nhập giá vé đêm")

        if self._card:
            self.txtCode.setText(self._card.card_code)
            self.txtCode.setReadOnly(True)
            self.txtNightPrice.setText(str(self._card.night_price))

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btnCancel = QPushButton("Hủy")
        self.btnCancel.setStyleSheet(
            """
            QPushButton {
                background-color: #95a5a6; color: white; border: none; 
                padding: 10px 30px; font-size: 14px; font-weight: 600; 
                border-radius: 6px; min-width: 100px;
            }
            QPushButton:hover { background-color: #7f8c8d; }
        """
        )
        self.btnCancel.clicked.connect(self.reject)

        self.btnSave = QPushButton("Lưu")
        self.btnSave.setStyleSheet(
            """
            QPushButton {
                background-color: #2E86C1; color: white; border: none; 
                padding: 10px 30px; font-size: 14px; font-weight: 600; 
                border-radius: 6px; min-width: 100px;
            }
            QPushButton:hover { background-color: #154360; }
        """
        )
        self.btnSave.clicked.connect(self.accept)

        btn_layout.addWidget(self.btnCancel)
        btn_layout.addWidget(self.btnSave)
        layout.addLayout(btn_layout)

        # Global Styles
        self.setStyleSheet(
            """
            QLineEdit { padding: 8px; border: 1px solid #dcdcdc; border-radius: 4px; font-size: 14px; background-color: white; }
            QLineEdit:focus { border: 2px solid #2E86C1; }
            QLabel { font-size: 14px; }
        """
        )

    def set_card_code(self, code):
        self.txtCode.setText(code)

    def _create_form_row(self, label_text, widget, parent_layout):
        row_layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setMinimumWidth(150)
        row_layout.addWidget(label)
        row_layout.addWidget(widget, 1)
        parent_layout.addLayout(row_layout)
        return widget

    def get_data(self):
        return {
            "card_code": self.txtCode.text(),
            "price": int(self.txtPrice.text() or 0),
            "night_price": int(self.txtNightPrice.text() or 0),
        }
