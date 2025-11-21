from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class LeftPanel(QWidget):
    """
    Khu vực cột trái: Thông tin Cảnh báo, Phí và Thông tin Thẻ.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setupUi()

    def _setupUi(self):
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(10)

        # Logo
        logoLabel = QLabel("GIỮ XE")
        logoLabel.setObjectName("ParkingLogo")
        vLayout.addWidget(logoLabel, alignment=Qt.AlignTop | Qt.AlignLeft)

        # --- 1. THÔNG TIN CẢNH BÁO / THÔNG TIN CHUNG ---
        titleInfoLabel = QLabel("THÔNG TIN CẢNH BÁO")
        titleInfoLabel.setObjectName("TitleLabel")
        vLayout.addWidget(titleInfoLabel)

        # Khung trạng thái
        statusFrame = QFrame()
        statusFrame.setObjectName("StatusFrame")
        statusFrame.setStyleSheet("background-color: #27ae60;")
        statusVLayout = QVBoxLayout(statusFrame)

        statusLabel1 = QLabel("KHÁCH HÀNG CÓ THẺ THÁNG")
        statusLabel1.setFont(QFont('Arial', 18, QFont.Bold))
        statusLabel1.setStyleSheet("color: white;")
        statusVLayout.addWidget(statusLabel1, alignment=Qt.AlignCenter)

        vLayout.addWidget(statusFrame)

        # --- Thông tin Biển số và Thời gian gửi ---
        infoWidget = QWidget()
        infoLayout = QGridLayout(infoWidget)
        infoLayout.setSpacing(8)

        # Hàng 0: Biển số Vào Label
        infoLayout.addWidget(QLabel("BIỂN SỐ VÀO"), 0, 0)

        # Hàng 1: Khung Biển số Vào (Plate Frame)
        bsVaoFrame = QFrame()
        bsVaoFrame.setFrameShape(QFrame.Box)  # Thiết lập hình dạng hộp
        bsVaoFrame.setFrameShadow(QFrame.Raised)
        # Thiết lập style cho khung biển số
        bsVaoFrame.setStyleSheet("""
            QFrame {
                padding: 10px;
                font-size: 26px;
                border-radius: 8px;
                background-color: #34495e; /* Nền tối hơn */
            }
        """)
        bsVaoVLayout = QVBoxLayout(bsVaoFrame)
        bsVaoVLayout.setContentsMargins(10, 5, 10, 5)  # Giảm margin bên trong

        bsVaoLabel = QLabel("20B1-073.64")
        bsVaoLabel.setFont(QFont('Arial', 36, QFont.Bold))
        bsVaoLabel.setStyleSheet("color: #3498db;")

        bsVaoVLayout.addWidget(bsVaoLabel, alignment=Qt.AlignCenter)
        infoLayout.addWidget(bsVaoFrame, 1, 0)  # Thêm frame vào layout

        # Hàng 2: Biển số Ra Label
        infoLayout.addWidget(QLabel("BIỂN SỐ RA"), 2, 0)

        # Hàng 3: Khung Biển số Ra (Plate Frame)
        bsRaFrame = QFrame()
        bsRaFrame.setFrameShape(QFrame.Box)
        bsRaFrame.setFrameShadow(QFrame.Raised)
        # Thiết lập style cho khung biển số
        bsRaFrame.setStyleSheet("""
            QFrame {
                padding: 10px;
                font-size: 26px;
                border-radius: 8px;
                background-color: #34495e; /* Nền tối hơn */
            }
        """)
        bsRaVLayout = QVBoxLayout(bsRaFrame)
        bsRaVLayout.setContentsMargins(10, 5, 10, 5)  # Giảm margin bên trong

        bsRaLabel = QLabel("20B1-073.64")
        bsRaLabel.setFont(QFont('Arial', 36, QFont.Bold))
        bsRaLabel.setStyleSheet("color: #3498db;")  # Đổi màu chữ sang trắng sáng

        bsRaVLayout.addWidget(bsRaLabel, alignment=Qt.AlignCenter)
        infoLayout.addWidget(bsRaFrame, 3, 0)  # Thêm frame vào layout

        # Hàng 4, 5: SỐ NGÀY GỬI
        durationLabel = QLabel("SỐ NGÀY GỬI")
        durationLabel.setStyleSheet("color: #95a5a6; font-size: 16px;")
        infoLayout.addWidget(durationLabel, 4, 0)

        durationValue = QLabel("1 NGÀY 08 GIỜ")
        durationValue.setFont(QFont('Arial', 18, QFont.Bold))
        durationValue.setStyleSheet("color: #f1c40f;")
        infoLayout.addWidget(durationValue, 5, 0, alignment=Qt.AlignHCenter)

        # Hàng 6: Phí giữ xe
        infoLayout.addWidget(QLabel("PHÍ GIỮ XE"), 6, 0)

        # Khung số tiền lớn
        feeFrame = QFrame()
        feeFrame.setObjectName("FeeFrame")
        feeFrame.setStyleSheet("background-color: #34495e;")
        feeVLayout = QVBoxLayout(feeFrame)

        fee_label = QLabel("0,000 VNĐ")
        fee_label.setObjectName("BigNumber")
        feeVLayout.addWidget(fee_label, alignment=Qt.AlignCenter)

        # Hàng 7: Khung Phí giữ xe
        infoLayout.addWidget(feeFrame, 7, 0, 1, 1)

        vLayout.addWidget(infoWidget)

        # --- 2. THÔNG TIN THẺ ---
        titleCardLabel = QLabel("THÔNG TIN THẺ")
        titleCardLabel.setObjectName("TitleLabel")
        vLayout.addWidget(titleCardLabel)

        cardFrame = QFrame()
        cardFrame.setObjectName("CardInfoFrame")
        cardFrame.setStyleSheet("background-color: #2c3e50;")
        cardGridLayout = QGridLayout(cardFrame)
        cardGridLayout.setSpacing(5)

        cardData = [
            ("CHỦ XE", "Nguyễn Minh Trí"),
            ("BIỂN SỐ ĐK", "20B1-073.64"),
            ("MÃ THẺ", ""),
            ("T/G XE VÀO", "24/10/2019 - 08:12:06"),
            ("T/G XE RA", "24/10/2019 - 16:17:51"),
            ("SỐ THẺ", "20739369"),
        ]

        for i, (labelText, valueText) in enumerate(cardData):
            label = QLabel(labelText)
            label.setStyleSheet("color: #95a5a6; font-size: 12px;")
            value = QLabel(valueText)
            value.setStyleSheet("color: #f1c40f; font-weight: bold;")

            cardGridLayout.addWidget(label, i, 0)
            cardGridLayout.addWidget(value, i, 1, alignment=Qt.AlignRight)

        vLayout.addWidget(cardFrame)

        vLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
