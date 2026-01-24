from model.Application import Application
from services.AIService import AIService


class StaffController:
    def __init__(self):
        self.__application = Application()
        self.__ai_service = AIService()
        self.__views = {}

    def add_view(self, name, view):
        self.__views[name] = view

    def process_entry(self, frame):
        frame, new_plates = self.__ai_service.process_frame(frame)

        if new_plates:
            left_view = self.__views["left"]
            try:
                if len(new_plates) > 1:
                    raise Exception("Phát hiện nhiều biển số, vui lòng quẹt lại")
                for plate in new_plates:
                    print(f"StaffController: entry {plate}")
                    card = self.__application.check_in(None, plate)
                    if card is None:
                        left_view.set_status("Không tìm thấy thẻ")
                    else:
                        right_view = self.__views["right"]
                        right_view.update_view(card)
                        left_view.update_view(card)
                        if frame is not None:
                            center_view = self.__views["center"]
                            center_view.set_frame(frame)
            except Exception as e:
                left_view.set_status(str(e))

    def process_exit(self, frame):
        frame, new_plates = self.__ai_service.process_frame(frame)

        if new_plates:
            left_view = self.__views["left"]
            try:
                if len(new_plates) > 1:
                    raise Exception("Phát hiện nhiều biển số, vui lòng quẹt lại")
                for plate in new_plates:
                    print(f"StaffController: exit {plate}")
                    card = self.__application.check_out(None, plate)
                    if card is None:
                        left_view.set_status("Không tìm thấy thẻ")
                    else:
                        right_view = self.__views["right"]
                        right_view.update_view(card)
                        left_view.update_view(card)
                        if frame is not None:
                            center_view = self.__views["center"]
                            center_view.set_frame(frame, start=2, stop=4)
            except Exception as e:
                left_view.set_status(str(e))