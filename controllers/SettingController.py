from model.Application import Application
from model.Settings import Settings


class SettingController:
    def __init__(self):
        self.__application = Application()
        self.__settings = Settings()
        self.__view = None

    def set_view(self, view):
        self.__view = view

    def load_data(self):
        self.__view.set_data(self.__settings)