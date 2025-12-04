import torch
import cv2

from modelAI.function import utils_rotate, helper


class LicensePlateRecognizer:
    """
    Module đóng gói phần model AI:
    - Load sẵn 2 model YOLOv5 đã train (.pt)
    - Cung cấp hàm xử lý 1 frame và trả về:
        + frame đã vẽ bbox + text
        + tập các biển số đọc được
    """

    def __init__(
        self,
        detector_weights: str = "LP_detector_nano_61.pt",
        ocr_weights: str = "LP_ocr_nano_62.pt",
        conf_threshold: float = 0.6,
    ) -> None:
        # Chỉ load model một lần khi khởi tạo class
        self.yolo_LP_detect = torch.hub.load(
            "ultralytics/yolov5",
            "custom",
            path=detector_weights,
            force_reload=False,
        )
        self.yolo_license_plate = torch.hub.load(
            "ultralytics/yolov5",
            "custom",
            path=ocr_weights,
            force_reload=False,
        )
        self.yolo_license_plate.conf = conf_threshold

    def process_frame(self, frame):
        """
        Nhận vào 1 frame (BGR – từ OpenCV),
        trả về (frame_đã_vẽ, set_biển_số_đọc_được)
        """
        results = self.yolo_LP_detect(frame)
        list_read_plates = set()

        for det in results.xyxy[0]:
            # YOLOv5 trả về tensor [x1, y1, x2, y2, conf, cls]
            x1, y1, x2, y2, conf, cls = det
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

            # Cắt vùng biển số
            crop_img = frame[y1:y2, x1:x2]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # OCR đọc biển số (giữ nguyên logic cũ)
            lp = ""
            for cc in range(0, 2):
                for ct in range(0, 2):
                    lp = helper.read_plate(
                        self.yolo_license_plate,
                        utils_rotate.deskew(crop_img, cc, ct),
                    )
                    if lp != "unknown":
                        list_read_plates.add(lp)
                        cv2.putText(
                            frame,
                            lp,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (36, 255, 12),
                            2,
                        )
                        break
                if lp != "unknown":
                    break

        return frame, list_read_plates


