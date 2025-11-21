from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
import cv2


class RightPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.entry_camera = None
        self.exit_camera = None
        self._setupUi()
        self._initCameras()

    def _setupUi(self):
        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(10)

        # --- CAMERA HÌNH ẢNH ---
        titleCameraLabel = QLabel("CAMERA HÌNH ẢNH (VÀO / RA)")
        titleCameraLabel.setObjectName("TitleLabel")
        vLayout.addWidget(titleCameraLabel, alignment=Qt.AlignTop | Qt.AlignRight)

        # --- Hai khung camera song song ---
        camerasFrame = QFrame()
        camerasLayout = QHBoxLayout(camerasFrame)
        camerasLayout.setContentsMargins(0, 0, 0, 0)
        camerasLayout.setSpacing(10)

        # Camera vào
        entryLayout = QVBoxLayout()
        entryTitle = QLabel("Camera VÀO")
        entryTitle.setStyleSheet("color: #2ecc71; font-weight: bold;")
        self.entryCameraLabel = QLabel()
        self.entryCameraLabel.setFixedSize(320, 240)
        self.entryCameraLabel.setStyleSheet("background-color: black; border: 2px solid #2ecc71;")
        self.entryCameraLabel.setAlignment(Qt.AlignCenter)
        entryLayout.addWidget(entryTitle, alignment=Qt.AlignCenter)
        entryLayout.addWidget(self.entryCameraLabel)

        # Camera ra
        exitLayout = QVBoxLayout()
        exitTitle = QLabel("Camera RA")
        exitTitle.setStyleSheet("color: #e74c3c; font-weight: bold;")
        self.exitCameraLabel = QLabel()
        self.exitCameraLabel.setFixedSize(320, 240)
        self.exitCameraLabel.setStyleSheet("background-color: black; border: 2px solid #e74c3c;")
        self.exitCameraLabel.setAlignment(Qt.AlignCenter)
        exitLayout.addWidget(exitTitle, alignment=Qt.AlignCenter)
        exitLayout.addWidget(self.exitCameraLabel)

        camerasLayout.addLayout(entryLayout)
        camerasLayout.addLayout(exitLayout)

        vLayout.addWidget(camerasFrame, alignment=Qt.AlignCenter)

        # --- CÁC LƯỢT VÀO RA GẦN ĐÂY ---
        titleHistoryLabel = QLabel("CÁC LƯỢT VÀO RA GẦN ĐÂY")
        titleHistoryLabel.setObjectName("TitleLabel")
        vLayout.addWidget(titleHistoryLabel)

        # Bảng
        historyTable = QTableWidget()
        historyTable.setRowCount(10)
        historyTable.setColumnCount(4)
        historyTable.setHorizontalHeaderLabels(["Biển số", "TG Vào", "TG Ra", "Trạng thái"])

        historyTable.setStyleSheet("""
            QTableWidget {
                gridline-color: #34495e;
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #34495e;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: #f1c40f;
                padding: 4px;
                border: 1px solid #34495e;
            }
        """)

        historyTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        historyTable.verticalHeader().setVisible(False)

        data_rows = [
            ("20A-123.45", "17:00", "17:05", "Đã ra"),
            ("30B-678.90", "17:01", "---", "Đang đỗ"),
            ("51C-111.22", "17:05", "17:06", "Đã ra"),
        ]

        for row, row_data in enumerate(data_rows):
            for col, item in enumerate(row_data):
                historyTable.setItem(row, col, QTableWidgetItem(item))

        vLayout.addWidget(historyTable)

        # Logo
        vdiLogoLabel = QLabel("VDI")
        vdiLogoLabel.setFont(QFont('Arial', 20, QFont.Bold))
        vdiLogoLabel.setStyleSheet("color: #3498db;")
        vLayout.addWidget(vdiLogoLabel, alignment=Qt.AlignBottom | Qt.AlignRight)

    def _initCameras(self):
        # --- Camera vào (index 0) ---
        self.entry_camera = cv2.VideoCapture(0)
        self.entry_timer = QTimer()
        self.entry_timer.timeout.connect(self._updateEntryFrame)
        self.entry_timer.start(30)

        # --- Camera ra (index 1) ---
        self.exit_camera = cv2.VideoCapture(1)
        self.exit_timer = QTimer()
        self.exit_timer.timeout.connect(self._updateExitFrame)
        self.exit_timer.start(30)

    def _updateEntryFrame(self):
        if not self.entry_camera:
            return

        ret, frame = self.entry_camera.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        qImg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg).scaled(self.entryCameraLabel.size(), Qt.KeepAspectRatio)
        self.entryCameraLabel.setPixmap(pixmap)

    def _updateExitFrame(self):
        if not self.exit_camera:
            return

        ret, frame = self.exit_camera.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        qImg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg).scaled(self.exitCameraLabel.size(), Qt.KeepAspectRatio)
        self.exitCameraLabel.setPixmap(pixmap)

    def closeEvent(self, event):
        if self.entry_camera:
            self.entry_timer.stop()
            self.entry_camera.release()
        if self.exit_camera:
            self.exit_timer.stop()
            self.exit_camera.release()
        super().closeEvent(event)
