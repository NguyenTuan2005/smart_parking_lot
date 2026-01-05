from PyQt6.QtWidgets import QMessageBox

from model.Application import Application
from model.Settings import Settings


class SettingController:
    def __init__(self):
        self.__application = Application()
        self.__settings = Settings()
        self.__view = None

    def set_view(self, view):
        self.__view = view

    def load_data(self) -> None:
        self.__view.set_data(self.__settings)

    def save_settings(self) -> None:
        try:
            monthly_fee = int(self.__view.monthly_fee_input.text())
            single_day_fee = int(self.__view.single_day_input.text())
            single_night_fee = int(self.__view.single_night_input.text())
            if not self.__settings.eq_monthly_fee(monthly_fee):
                self.__settings.monthly_fee = monthly_fee

            if not self.__settings.eq_single_day_fee(single_day_fee):
                self.__application.apply_single_day_fee(single_day_fee)
                self.__settings.single_day_fee = single_day_fee

            if not self.__settings.eq_single_night_fee(single_night_fee):
                self.__application.apply_single_night_fee(single_night_fee)
                self.__settings.single_night_fee = single_night_fee
        except ValueError:
            QMessageBox.critical(self.__view, "Lỗi", "Giá trị không hợp lệ!!")
            return
        self.__settings.total_slots = self.__view.slots_spin.value()

        try:
            self.__settings.save_data()
        except Exception as e:
            raise Exception(e) from e
