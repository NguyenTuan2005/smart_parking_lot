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
            for plate in new_plates:
                card = self.__application.check_in(None, plate)
                print(f"StaffController: {card}")

                right_view = self.__views["right"]
                right_view.update_view(card)
                left_view = self.__views["left"]
                left_view.update_view(card)
                if frame is not None:
                    center_view = self.__views["center"]
                    center_view.set_frame(frame)