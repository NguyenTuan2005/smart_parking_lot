import os
import torch
from modelAI.function import utils_rotate as utils_rotate
from modelAI.function import helper as helper

class AIService:
    def __init__(self):
        self._load_models()

    def _load_models(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))  # services folder
            project_root = os.path.dirname(current_dir)  # go up to project root
            model_dir = os.path.join(project_root, 'modelAI')

            lp_detector_path = os.path.join(model_dir, 'LP_detector_nano_61.pt')
            lp_ocr_path = os.path.join(model_dir, 'LP_ocr_nano_62.pt')

            self.yolo_LP_detect = torch.hub.load('ultralytics/yolov5', 'custom',
                                                 path=lp_detector_path, force_reload=True)
            self.yolo_license_plate = torch.hub.load('ultralytics/yolov5', 'custom',
                                                     path=lp_ocr_path, force_reload=True)
            self.yolo_license_plate.conf = 0.6
        except Exception as e:
            print(f"Error loading models: {e}")
            self.yolo_LP_detect = None
            self.yolo_license_plate = None

    def get_vehicle(self, frame):
        if frame is None or self.yolo_LP_detect is None:
            return None

        results = self.yolo_LP_detect(frame)
        detected_plates = []

        for det in results.xyxy[0]:
            x1, y1, x2, y2, conf = det
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

            crop_img = frame[y1:y2, x1:x2]

            license_plate = self._read_license_plate(crop_img)

            if license_plate != "unknown":
                vehicle_data = {
                    'license_plate': license_plate,
                    'bbox': (x1, y1, x2, y2),
                    'confidence': float(conf),
                    'crop_image': crop_img
                }
                detected_plates.append(vehicle_data)

        return detected_plates[0] if detected_plates else None

    def _read_license_plate(self, crop_img):
        if self.yolo_license_plate is None:
            return "unknown"

        for cc in range(0, 2):
            for ct in range(0, 2):
                try:
                    processed_img = utils_rotate.deskew(crop_img, cc, ct)
                    license_plate = helper.read_plate(self.yolo_license_plate, processed_img)
                    if license_plate != "unknown":
                        return license_plate
                except Exception as e:
                    continue

        return "unknown"