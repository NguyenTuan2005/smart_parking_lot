from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from controllers.StaffController import StaffController
from model.Card import Card
from model.MonthlyCard import MonthlyCard


class LeftPanel(QWidget):
    """
    Khu vực cột trái: Thông tin Cảnh báo, Phí và Thông tin Thẻ.
    (Đã tối ưu hóa kích thước cho PyQt6)
    """

    def __init__(self, controller: StaffController, parent=None):
        super().__init__(parent)
        self.__controller = controller
        controller.add_view("left", self)
        self._setupUi()

    def _setupUi(self):
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(8)  # Giảm spacing tổng thể

        # Logo
        logoLabel = QLabel("GIỮ XE")
        logoLabel.setObjectName("ParkingLogo")
        vLayout.addWidget(logoLabel, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # --- 1. THÔNG TIN CẢNH BÁO / THÔNG TIN CHUNG ---
        titleInfoLabel = QLabel("THÔNG TIN CẢNH BÁO")
        titleInfoLabel.setObjectName("TitleLabel")
        vLayout.addWidget(titleInfoLabel)

        # Khung trạng thái
        statusFrame = QFrame()
        statusFrame.setObjectName("StatusFrame")
        statusFrame.setStyleSheet("background-color: #2c3e50;")
        statusVLayout = QVBoxLayout(statusFrame)

        self.__statusLabel1 = QLabel("KHÁCH HÀNG CÓ THẺ THÁNG")
        self.__statusLabel1.setFont(QFont('Arial', 16, weight=QFont.Weight.Bold))  # Giảm font
        self.__statusLabel1.setStyleSheet("color: white;")
        statusVLayout.addWidget(self.__statusLabel1, alignment=Qt.AlignmentFlag.AlignCenter)

        vLayout.addWidget(statusFrame)

        # --- Thông tin Biển số và Thời gian gửi ---
        infoWidget = QWidget()
        infoLayout = QGridLayout(infoWidget)
        infoLayout.setSpacing(6)  # Giảm spacing

        # Hàng 0: Biển số Vào Label
        infoLayout.addWidget(QLabel("BIỂN SỐ VÀO"), 0, 0)

        # Hàng 1: Khung Biển số Vào (Plate Frame)
        bsVaoFrame = QFrame()
        bsVaoFrame.setFrameShape(QFrame.Shape.Box)
        bsVaoFrame.setFrameShadow(QFrame.Shadow.Raised)
        # Tối ưu hóa Style
        bsVaoFrame.setStyleSheet("""
            QFrame {
                padding: 6px; /* Giảm padding */
                font-size: 22px; 
                border-radius: 6px; /* Giảm border-radius */
                background-color: #34495e; 
            }
        """)
        bsVaoVLayout = QVBoxLayout(bsVaoFrame)
        bsVaoVLayout.setContentsMargins(8, 3, 8, 3)  # Giảm margin

        self.__bsVaoLabel = QLabel("Trống")
        self.__bsVaoLabel.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))  # Giảm font
        self.__bsVaoLabel.setStyleSheet("color: #f1c40f;")

        bsVaoVLayout.addWidget(self.__bsVaoLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        infoLayout.addWidget(bsVaoFrame, 1, 0)

        # Hàng 2: Biển số Ra Label
        infoLayout.addWidget(QLabel("BIỂN SỐ RA"), 2, 0)

        # Hàng 3: Khung Biển số Ra (Plate Frame)
        bsRaFrame = QFrame()
        bsRaFrame.setFrameShape(QFrame.Shape.Box)
        bsRaFrame.setFrameShadow(QFrame.Shadow.Raised)
        # Tối ưu hóa Style
        bsRaFrame.setStyleSheet("""
            QFrame {
                padding: 6px;
                font-size: 22px;
                border-radius: 6px;
                background-color: #34495e;
            }
        """)
        bsRaVLayout = QVBoxLayout(bsRaFrame)
        bsRaVLayout.setContentsMargins(8, 3, 8, 3)

        self.__bsRaLabel = QLabel("Trống")
        self.__bsRaLabel.setFont(QFont('Arial', 30, weight=QFont.Weight.Bold))  # Giảm font
        self.__bsRaLabel.setStyleSheet("color: #f1c40f;")

        bsRaVLayout.addWidget(self.__bsRaLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        infoLayout.addWidget(bsRaFrame, 3, 0)

        # Hàng 4, 5: SỐ NGÀY GỬI
        durationLabel = QLabel("SỐ NGÀY GỬI")
        durationLabel.setStyleSheet("color: #95a5a6; font-size: 14px;")  # Giảm font
        infoLayout.addWidget(durationLabel, 4, 0)

        self.__durationValue = QLabel("1 NGÀY 08 GIỜ")
        self.__durationValue.setFont(QFont('Arial', 16, weight=QFont.Weight.Bold))  # Giảm font
        self.__durationValue.setStyleSheet("color: #f1c40f;")
        infoLayout.addWidget(self.__durationValue, 5, 0, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Hàng 6: Phí giữ xe
        infoLayout.addWidget(QLabel("PHÍ GIỮ XE"), 6, 0)

        # Khung số tiền lớn
        feeFrame = QFrame()
        feeFrame.setObjectName("FeeFrame")
        feeFrame.setStyleSheet("background-color: #34495e;")
        feeVLayout = QVBoxLayout(feeFrame)

        self.__fee_label = QLabel("0 VNĐ")
        self.__fee_label.setObjectName("BigNumber")
        feeVLayout.addWidget(self.__fee_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Hàng 7: Khung Phí giữ xe
        infoLayout.addWidget(feeFrame, 7, 0, 1, 1)

        # --- QUAN TRỌNG: Thêm giãn cách vào cột 1 để QGridLayout giãn ra hết chiều rộng ---
        infoLayout.setColumnStretch(1, 1)

        vLayout.addWidget(infoWidget)

        # --- 2. THÔNG TIN THẺ ---
        titleCardLabel = QLabel("THÔNG TIN THẺ")
        titleCardLabel.setObjectName("TitleLabel")
        vLayout.addWidget(titleCardLabel)

        cardFrame = QFrame()
        cardFrame.setObjectName("CardInfoFrame")
        cardFrame.setStyleSheet("background-color: #2c3e50;")
        cardGridLayout = QGridLayout(cardFrame)
        cardGridLayout.setSpacing(4)  # Giảm spacing

        cardData = [
            ("CHỦ XE", "Nguyễn Minh Trí"),
            ("BIỂN SỐ ĐK", "20B1-073.64"),
            ("MÃ THẺ", ""),
            ("T/G XE VÀO", "24/10/2019 - 08:12:06"),
            ("T/G XE RA", "24/10/2019 - 16:17:51"),
            ("SỐ THẺ", "20739369"),
        ]

        self.__card_info_labels = {}
        for i, (labelText, valueText) in enumerate(cardData):
            label = QLabel(labelText)
            label.setStyleSheet("color: #95a5a6; font-size: 11px;")  # Giảm font
            value = QLabel(valueText)
            value.setStyleSheet("color: #f1c40f; font-weight: bold; font-size: 12px;")  # Giảm font

            cardGridLayout.addWidget(label, i, 0)
            cardGridLayout.addWidget(value, i, 1, alignment=Qt.AlignmentFlag.AlignRight)
            self.__card_info_labels[labelText] = value

        # Giãn cách cho cột dữ liệu
        cardGridLayout.setColumnStretch(1, 1)

        vLayout.addWidget(cardFrame)

        # Giãn cách cuối cùng để đẩy tất cả lên trên
        vLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                          QSizePolicy.Policy.Expanding))

    def update_view(self, card: Card):

        if card.is_month_card():
            monthly: MonthlyCard = card
            self.__bsVaoLabel.setText(monthly.vehicle.plate_number)
            self.__card_info_labels["BIỂN SỐ ĐK"].setText(monthly.vehicle.plate_number)
            self.__card_info_labels["MÃ THẺ"].setText(monthly.card_code)
            self.__card_info_labels["SỐ THẺ"].setText(str(monthly.card_id))
            self.__card_info_labels["CHỦ XE"].setText(str(monthly.customer.fullname))
            self.__statusLabel1.setText("KHÁCH HÀNG CÓ THẺ THÁNG")
        else:
            self.__bsVaoLabel.setText(card.card_log.vehicle.plate_number)
            self.__bsRaLabel.setText("" if card.card_log.exit_at is None else str(card.card_log.exit_at))
            self.__durationValue.setText(str(card.duration()))
            self.__fee_label.setText(f"{card.calculate_fee()} VNĐ")
            self.__card_info_labels["BIỂN SỐ ĐK"].setText(card.card_log.vehicle.plate_number)
            self.__card_info_labels["MÃ THẺ"].setText(card.card_code)
            self.__card_info_labels["T/G XE VÀO"].setText(str(card.card_log.entry_at))
            self.__card_info_labels["T/G XE RA"].setText("" if card.card_log.exit_at is None else str(card.card_log.exit_at))
            self.__card_info_labels["SỐ THẺ"].setText(str(card.card_id))
            self.__card_info_labels["CHỦ XE"].setText("KHÁCH VÃNG LAI")
            self.__statusLabel1.setText("THẺ LẺ")

    def set_status(self, message: str):
        self.__statusLabel1.setText(message)