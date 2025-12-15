
import cv2
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QSizePolicy
)
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtCore import Qt

from controllers.StaffController import StaffController


class CenterPanel(QWidget):
    """
    Khu vực giữa chứa 4 khung Ảnh lớn.
    """

    def __init__(self, controller: StaffController, parent=None):
        super().__init__(parent)
        self.imagePaths = [
            "../../assets/images/xevao_1.jpg",
            "../../assets/images/xevao_1.jpg",
            "../../assets/images/xera_1.jpg",
            "../../assets/images/xera_1.jpg",
        ]
        self.imgLabels = []  # Lưu trữ các QLabel để dễ dàng truy cập lại
        self.__controller = controller
        controller.add_view("center", self)
        self._setupUi()

    def _setupUi(self):
        self.__gridLayout = QGridLayout(self)
        self.__gridLayout.setContentsMargins(0, 0, 0, 0)
        self.__gridLayout.setSpacing(5)

        imgIndex = 0

        # 4 Khung Video
        for i in range(2):
            for j in range(2):
                videoFrame = QFrame()
                videoFrame.setObjectName("VideoFrame")
                # Bỏ setMinimumSize để QGridLayout quản lý tốt hơn.
                # videoFrame.setMinimumSize(400, 300)
                # Đặt chính sách mở rộng
                videoFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

                frameVLayout = QVBoxLayout(videoFrame)
                frameVLayout.setContentsMargins(5, 5, 5, 5)  # Giảm margin để tối ưu không gian

                # Logic tạo label
                if i == 0:
                    baseText = "HÌNH ẢNH XE VÀO"
                    timeText = "24/10/2024 08:12:06"
                    labelStyle = "color: white;"
                else:
                    baseText = "HÌNH ẢNH XE RA"
                    timeText = "24/10/2024 16:17:51"
                    labelStyle = "color: white;"

                labelText = f"{baseText} - {timeText}"

                videoLabel = QLabel(labelText)
                # Giảm font size xuống 12px để phù hợp với DPI scaling của Qt6
                videoLabel.setFont(QFont('Arial', 12, weight=QFont.Weight.Bold))
                videoLabel.setStyleSheet(
                    f"background-color: rgba(0, 0, 0, 180); padding: 4px; border-radius: 3px; {labelStyle}"
                )
                frameVLayout.addWidget(videoLabel, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

                # --- PHẦN ĐIỀU CHỈNH CHÍNH ---
                imgLabel = QLabel()
                imgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                imgLabel.setStyleSheet("border: 1px solid #ffffff;")

                # 1. Tải Pixmap
                pixmap = QPixmap(self.imagePaths[imgIndex])
                imgLabel.original_pixmap = pixmap  # Lưu bản gốc
                imgLabel.setMaximumWidth(245)
                # 2. BẬT co giãn nội dung (Quan trọng)
                imgLabel.setScaledContents(True)

                # 3. Hiển thị ảnh (Ban đầu, chỉ hiển thị ảnh gốc hoặc ảnh scaled nhỏ)
                imgLabel.setPixmap(pixmap.scaled(
                    imgLabel.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
                self.imgLabels.append(imgLabel)  # Lưu nhãn vào danh sách
                imgIndex += 1

                frameVLayout.addWidget(imgLabel)
                self.__gridLayout.addWidget(videoFrame, i, j)

    def set_frame(self, frame):
        if frame is None:
            return

        height, width, channel = frame.shape
        bytes_per_line = 3 * width

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        if pixmap.isNull():
            return

        for idx in range(2):
            imgLabel = self.imgLabels[idx]
            imgLabel.original_pixmap = pixmap
            imgLabel.setPixmap(pixmap.scaled(
                imgLabel.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))