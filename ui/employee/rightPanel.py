# Sửa lỗi: Thay đổi cách truy cập hằng số KeepAspectRatio
# Tối ưu: Đặt QImage.Format_RGB888 cho rõ ràng hơn (dù đã là default)
# Tối ưu: Thay đổi index camera ra để tránh xung đột nếu có 2 webcam

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QFileDialog
)
from PyQt6.QtGui import QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
import cv2

from controllers.StaffController import StaffController
from model.Card import Card


class RightPanel(QWidget):
    def __init__(self, controller: StaffController, parent=None):
        super().__init__(parent)
        self.__controller = controller
        controller.add_view('right', self)
        self.entry_camera = None
        self.exit_camera = None
        # modes: 'camera' or 'upload' for each side
        self.mode = 'camera'  # entry mode
        self.mode_exit = 'camera'  # exit mode
        self.upload_capture = None
        self.upload_timer = None
        self.upload_capture_exit = None
        self.upload_timer_exit = None
        self._setupUi()
        self._initCameras()

    def _setupUi(self):

        vLayout = QVBoxLayout(self)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vLayout.setSpacing(10)

        # ... (Phần UI không thay đổi) ...
        # --- CAMERA HÌNH ẢNH ---
        titleCameraLabel = QLabel("CAMERA HÌNH ẢNH (VÀO / RA)")
        titleCameraLabel.setObjectName("TitleLabel")
        vLayout.addWidget(titleCameraLabel, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # Nút chuyển chế độ camera / upload
        # Nút chuyển chế độ camera / upload cho cả VÀO và RA
        btnRow = QHBoxLayout()
        btnRow.setContentsMargins(0, 0, 0, 0)
        btnRow.setSpacing(8)

        self.modeButtonEntry = QPushButton("Upload VÀO")
        self.modeButtonEntry.setFixedWidth(120)
        self.modeButtonEntry.clicked.connect(self._toggle_mode)
        btnRow.addStretch(1)
        btnRow.addWidget(self.modeButtonEntry)

        self.modeButtonExit = QPushButton("Upload RA")
        self.modeButtonExit.setFixedWidth(120)
        self.modeButtonExit.clicked.connect(self._toggle_mode_exit)
        btnRow.addWidget(self.modeButtonExit)

        vLayout.addLayout(btnRow)

        # --- Hai khung camera song song ---
        camerasFrame = QFrame()
        camerasLayout = QHBoxLayout(camerasFrame)
        camerasLayout.setContentsMargins(0, 0, 0, 0)
        camerasLayout.setSpacing(10)

        # Camera vào
        entryLayout = QVBoxLayout()
        entryTitle = QLabel("Camera VÀO")
        entryTitle.setStyleSheet("color: white; font-weight: bold;")
        self.entryCameraLabel = QLabel()
        self.entryCameraLabel.setFixedSize(320, 240)
        self.entryCameraLabel.setStyleSheet("background-color: black; border: 2px solid #ffffff;")
        self.entryCameraLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        entryLayout.addWidget(entryTitle, alignment=Qt.AlignmentFlag.AlignCenter)
        entryLayout.addWidget(self.entryCameraLabel)

        # Camera ra
        exitLayout = QVBoxLayout()
        exitTitle = QLabel("Camera RA")
        exitTitle.setStyleSheet("color: white; font-weight: bold;")
        self.exitCameraLabel = QLabel()
        self.exitCameraLabel.setFixedSize(320, 240)
        self.exitCameraLabel.setStyleSheet("background-color: black; border: 2px solid #ffffff;")
        self.exitCameraLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        exitLayout.addWidget(exitTitle, alignment=Qt.AlignmentFlag.AlignCenter)
        exitLayout.addWidget(self.exitCameraLabel)

        camerasLayout.addLayout(entryLayout)
        camerasLayout.addLayout(exitLayout)

        vLayout.addWidget(camerasFrame, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- CÁC LƯỢT VÀO RA GẦN ĐÂY ---
        titleHistoryLabel = QLabel("CÁC LƯỢT VÀO RA GẦN ĐÂY")
        titleHistoryLabel.setObjectName("TitleLabel")
        vLayout.addWidget(titleHistoryLabel)

        # Bảng
        self.__historyTable = QTableWidget()
        self.__historyTable.setRowCount(10)
        self.__historyTable.setColumnCount(4)
        self.__historyTable.setHorizontalHeaderLabels(["Biển số", "TG Vào", "TG Ra", "Trạng thái"])

        # Sử dụng Style đã tối ưu (đảm bảo QTableWidget style được áp dụng đúng)
        self.__historyTable.setStyleSheet("""
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

        self.__historyTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.__historyTable.verticalHeader().setVisible(False)

        data_rows = [
            ("20A-123.45", "17:00", "17:05", "Đã ra"),
            ("30B-678.90", "17:01", "---", "Đang đỗ"),
            ("51C-111.22", "17:05", "17:06", "Đã ra"),
        ]

        for row, row_data in enumerate(data_rows):
            for col, item in enumerate(row_data):
                self.__historyTable.setItem(row, col, QTableWidgetItem(item))

        vLayout.addWidget(self.__historyTable)

        # Logo
        vdiLogoLabel = QLabel("VDI")
        vdiLogoLabel.setFont(QFont('Arial', 20, weight=QFont.Weight.Bold))
        vdiLogoLabel.setStyleSheet("color: #ffffff;")
        vLayout.addWidget(vdiLogoLabel, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

    def _initCameras(self):
        # --- Camera vào (index 0) ---
        self.entry_camera = cv2.VideoCapture(0)  # Đặt index 0
        self.entry_timer = QTimer()
        self.entry_timer.timeout.connect(self._updateEntryFrame)
        # Chỉ khởi động timer nếu camera mở thành công
        if self.entry_camera.isOpened():
            self.entry_timer.start(30)  # 30ms ~ 33 FPS

        # --- Camera ra (index 1 hoặc 2) ---
        self.exit_camera = cv2.VideoCapture(1)  # Đặt index 1 (hoặc 2 nếu index 1 không có)
        self.exit_timer = QTimer()
        self.exit_timer.timeout.connect(self._updateExitFrame)
        if self.exit_camera.isOpened():
            self.exit_timer.start(30)

    def _updateEntryFrame(self):
        if not self.entry_camera or not self.entry_camera.isOpened():
            return

        ret, frame = self.entry_camera.read()
        if not ret:
            return

        # Process frame through controller if needed
        try:
            self.__controller.process_entry(frame)
        except Exception:
            pass

        # Convert color and show
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qImg = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0],
                      QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg).scaled(self.entryCameraLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.entryCameraLabel.setPixmap(pixmap)

    def _updateUploadFrame(self):
        if not self.upload_capture or not self.upload_capture.isOpened():
            return

        ret, frame = self.upload_capture.read()
        # If video ended, loop to start
        if not ret:
            try:
                self.upload_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.upload_capture.read()
            except Exception:
                return

        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qImg = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0],
                      QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg).scaled(self.entryCameraLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.entryCameraLabel.setPixmap(pixmap)

    def _updateUploadFrameExit(self):
        if not self.upload_capture_exit or not self.upload_capture_exit.isOpened():
            return

        ret, frame = self.upload_capture_exit.read()
        # If video ended, loop to start
        if not ret:
            try:
                self.upload_capture_exit.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.upload_capture_exit.read()
            except Exception:
                return

        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qImg = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0],
                      QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg).scaled(self.exitCameraLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.exitCameraLabel.setPixmap(pixmap)

    def _toggle_mode_exit(self):
        # Switch between live camera and uploaded video for the EXIT camera
        if self.mode_exit == 'camera':
            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn video (RA)", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)")
            if not file_path:
                return

            # stop and release exit camera timer/capture
            if self.exit_camera and self.exit_camera.isOpened():
                try:
                    self.exit_timer.stop()
                except Exception:
                    pass
                try:
                    self.exit_camera.release()
                except Exception:
                    pass

            # open video file for exit
            self.upload_capture_exit = cv2.VideoCapture(file_path)
            if not self.upload_capture_exit.isOpened():
                return
            self.upload_timer_exit = QTimer()
            self.upload_timer_exit.timeout.connect(self._updateUploadFrameExit)
            self.upload_timer_exit.start(30)
            self.mode_exit = 'upload'
            self.modeButtonExit.setText('Dùng RA')
        else:
            # stop upload playback
            if getattr(self, 'upload_timer_exit', None):
                try:
                    self.upload_timer_exit.stop()
                except Exception:
                    pass
            if getattr(self, 'upload_capture_exit', None):
                try:
                    self.upload_capture_exit.release()
                except Exception:
                    pass

            # restart exit camera
            self.exit_camera = cv2.VideoCapture(1)
            if self.exit_camera.isOpened():
                try:
                    self.exit_timer.start(30)
                except Exception:
                    pass
            self.mode_exit = 'camera'
            self.modeButtonExit.setText('Upload RA')

    def _toggle_mode(self):
        # Switch between live camera and uploaded video for the ENTRY camera
        if self.mode == 'camera':
            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn video", "", "Video Files (*.mp4 *.avi *.mov);;All Files (*)")
            if not file_path:
                return

            # stop and release camera
            if self.entry_camera and self.entry_camera.isOpened():
                try:
                    self.entry_timer.stop()
                except Exception:
                    pass
                try:
                    self.entry_camera.release()
                except Exception:
                    pass

            # open video file
            self.upload_capture = cv2.VideoCapture(file_path)
            if not self.upload_capture.isOpened():
                return
            self.upload_timer = QTimer()
            self.upload_timer.timeout.connect(self._updateUploadFrame)
            self.upload_timer.start(30)
            self.mode = 'upload'
            self.modeButtonEntry.setText('Dùng VÀO')
        else:
            # stop upload playback
            if getattr(self, 'upload_timer', None):
                try:
                    self.upload_timer.stop()
                except Exception:
                    pass
            if getattr(self, 'upload_capture', None):
                try:
                    self.upload_capture.release()
                except Exception:
                    pass

            # restart camera
            self.entry_camera = cv2.VideoCapture(0)
            if self.entry_camera.isOpened():
                try:
                    self.entry_timer.start(30)
                except Exception:
                    pass
            self.mode = 'camera'
            self.modeButtonEntry.setText('Upload VÀO')

    def _updateExitFrame(self):
        if not self.exit_camera or not self.exit_camera.isOpened():  # Kiểm tra isOpened()
            return

        ret, frame = self.exit_camera.read()
        if not ret:
            return

        # Tối ưu hóa: Bỏ cv2.flip(frame, 1) nếu camera không bị lật
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Sửa lỗi: Qt.KeepAspectRatio -> Qt.AspectRatioMode.KeepAspectRatio
        qImg = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0],
                      QImage.Format.Format_RGB888)  # Thêm bước để ổn định hơn
        pixmap = QPixmap.fromImage(qImg).scaled(self.exitCameraLabel.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.exitCameraLabel.setPixmap(pixmap)

    def closeEvent(self, event):
        if self.entry_camera:
            self.entry_timer.stop()
            self.entry_camera.release()
        if self.exit_camera:
            self.exit_timer.stop()
            self.exit_camera.release()
        super().closeEvent(event)

    def update_view(self, card: Card):
        plate = card.vehicle.plate_number if card.vehicle else "---"
        time_entry = card.time_entry.strftime("%H:%M") if card.time_entry else "---"
        time_exit = card.time_exit.strftime("%H:%M") if card.time_exit else "---"
        status = "Đã ra" if card.time_exit else "Đang đỗ"

        row_count = self.__historyTable.rowCount()
        col_count = self.__historyTable.columnCount()
        for r in range(row_count - 1, 0, -1):
            for c in range(col_count):
                src = self.__historyTable.item(r - 1, c)
                self.__historyTable.setItem(r, c, QTableWidgetItem(src.text() if src else ""))

        self.__historyTable.setItem(0, 0, QTableWidgetItem(plate))
        self.__historyTable.setItem(0, 1, QTableWidgetItem(time_entry))
        self.__historyTable.setItem(0, 2, QTableWidgetItem(time_exit))
        self.__historyTable.setItem(0, 3, QTableWidgetItem(status))