from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt


class CenterPanel(QWidget):
    """
    Khu vực giữa chứa 4 khung Ảnh lớn.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setupUi()

    def _setupUi(self):
        gridLayout = QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setSpacing(5)

        # Danh sách ảnh mẫu (thay bằng ảnh của bạn)
        imagePaths = [
            "../assets/images/xevao_1.jpg",
            "../assets/images/xevao_1.jpg",
            "../assets/images/xera_1.jpg",
            "../assets/images/xera_1.jpg",
        ]

        imgIndex = 0

        # 4 Khung Video
        for i in range(2):
            for j in range(2):
                videoFrame = QFrame()
                videoFrame.setObjectName("VideoFrame")
                videoFrame.setMinimumSize(400, 300)
                videoFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                frameVLayout = QVBoxLayout(videoFrame)
                frameVLayout.setContentsMargins(10, 10, 10, 10)

                # Xác định nhãn và thời gian dựa trên hàng (i)
                if i == 0:
                    baseText = "HÌNH ẢNH XE VÀO"
                    timeText = "24/10/2024 08:12:06"
                    labelStyle = "color: #2ecc71;"
                else:
                    baseText = "HÌNH ẢNH XE RA"
                    timeText = "24/10/2024 16:17:51"
                    labelStyle = "color: #e74c3c;"

                labelText = f"{baseText} - {timeText}"

                videoLabel = QLabel(labelText)
                videoLabel.setFont(QFont('Arial', 14, QFont.Bold))
                videoLabel.setStyleSheet(
                    f"background-color: rgba(0, 0, 0, 180); padding: 5px; border-radius: 4px; {labelStyle}"
                )
                frameVLayout.addWidget(videoLabel, alignment=Qt.AlignTop | Qt.AlignLeft)

                imgLabel = QLabel()
                imgLabel.setAlignment(Qt.AlignCenter)
                imgLabel.setStyleSheet("border: 2px solid #3498db;")
                pixmap = QPixmap(imagePaths[imgIndex])
                imgLabel.setPixmap(pixmap.scaled(700, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                imgIndex += 1

                frameVLayout.addWidget(imgLabel)

                gridLayout.addWidget(videoFrame, i, j)

