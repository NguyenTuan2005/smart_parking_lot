import os
import re
import time

from modelAI import LicensePlateRecognizer


class AIService:
    def __init__(self):
        self._load_models()
        self._recent_plates = {}
        self._cooldown_seconds = 3

    def _load_models(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            model_dir = os.path.join(project_root, 'modelAI')

            lp_detector_path = os.path.join(model_dir, 'LP_detector_nano_61.pt')
            lp_ocr_path = os.path.join(model_dir, 'LP_ocr_nano_62.pt')
            self.__lp_recognizer = LicensePlateRecognizer(detector_weights=lp_detector_path,
                                                          ocr_weights=lp_ocr_path)
        except Exception as e:
            print(f"Error loading models: {e}")
            self.__lp_recognizer = None

    def process_frame(self, frame):
        if frame is None or self.__lp_recognizer is None:
            return None, []

        frame, list_read_plates = self.__lp_recognizer.process_frame(frame)

        current_time = time.time()
        new_plates = []

        for plate in list_read_plates:
            if not self._recent_plates.__contains__(plate) and self.valid_plate(plate):
                last_seen = self._recent_plates.get(plate, 0)
                if current_time - last_seen > self._cooldown_seconds:
                    new_plates.append(plate)
                    self._recent_plates[plate] = current_time

        self._cleanup_old_plates(current_time)

        return frame, new_plates

    def valid_plate(self, plate) -> bool:
        if len(plate) == 10:
            pattern = r'^[0-9]{2}[A-Z]{1,2}[0-9]-[0-9]{4,5}$'
            return re.match(pattern, plate) is not None
        return False

    def _cleanup_old_plates(self, current_time):
        remove_list = [plate for plate, timestamp in self._recent_plates.items()
                       if current_time - timestamp > 60]
        for plate in remove_list:
            del self._recent_plates[plate]
