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
        self.imagePaths = [
            "../../assets/images/xevao_1.jpg",
            "../../assets/images/xevao_1.jpg",
            "../../assets/images/xera_1.jpg",
            "../../assets/images/xera_1.jpg",
        ]
        self.imgLabels = []  # Lưu trữ các QLabel để dễ dàng truy cập lại
        self._setupUi()

    def _setupUi(self):
        gridLayout = QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.setSpacing(5)

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
                    labelStyle = "color: #2ecc71;"
                else:
                    baseText = "HÌNH ẢNH XE RA"
                    timeText = "24/10/2024 16:17:51"
                    labelStyle = "color: #e74c3c;"

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
                imgLabel.setStyleSheet("border: 1px solid #3498db;")

                # 1. Tải Pixmap
                pixmap = QPixmap(self.imagePaths[imgIndex])
                imgLabel.original_pixmap = pixmap  # Lưu bản gốc

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
                gridLayout.addWidget(videoFrame, i, j)

    # --- THÊM PHƯƠNG THỨC RESIZE EVENT (Tùy chọn, nếu setScaledContents(True) chưa đủ) ---
    def resizeEvent(self, event):
        """
        Đảm bảo hình ảnh được co giãn lại mỗi khi widget thay đổi kích thước.
        (Thường không cần thiết nếu dùng setScaledContents(True) và QGridLayout,
        nhưng hữu ích khi cần kiểm soát chính xác hơn).
        """
        for label in self.imgLabels:
            if hasattr(label, 'original_pixmap') and not label.original_pixmap.isNull():
                # Lấy kích thước hiện tại của QLabel để co giãn ảnh theo đó
                scaled_pixmap = label.original_pixmap.scaled(
                    label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)