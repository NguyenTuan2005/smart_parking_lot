from model.Application import Application
from services.AIService import AIService

class AIController:
    def __init__(self):
        self.__application = Application()
        self.__ai_service = AIService()
        self.__views = {}

    def add_view(self, name, view):
        self.__views[name] = view

    def process_entry(self, view_name, frame):
        vehicle = self.__ai_service.get_vehicle(frame)

        print (vehicle)
        # if len(self.__views) > 0:
        #     view = self.__views[view_name]
        #     view.show_entry(vehicle)