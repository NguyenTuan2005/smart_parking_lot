import json
from pathlib import Path

class Settings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.__total_slots = 250
        self.__monthly_fee = 150000
        self.__single_day_fee = 3000
        self.__single_night_fee = 5000

        self.__settings_file = Path("settings.json")
        if self.__settings_file.exists():
            with open(self.__settings_file, "r") as file:
                data = json.load(file)
                self.__total_slots = data.get("total_slots", self.__total_slots)
                self.__monthly_fee = data.get("monthly_fee", self.__monthly_fee)
                self.__single_day_fee = data.get("single_day_fee", self.__single_day_fee)
                self.__single_night_fee = data.get("single_night_fee", self.__single_night_fee)

    @property
    def total_slots(self):
        return self.__total_slots

    @total_slots.setter
    def total_slots(self, value: int):
        self.__total_slots = value

    @property
    def monthly_fee(self):
        return self.__monthly_fee

    @monthly_fee.setter
    def monthly_fee(self, value: int):
        self.__monthly_fee = value

    @property
    def single_day_fee(self):
        return self.__single_day_fee

    @single_day_fee.setter
    def single_day_fee(self, value: int):
        self.__single_day_fee = value

    @property
    def single_night_fee(self):
        return self.__single_night_fee

    @single_night_fee.setter
    def single_night_fee(self, value: int):
        self.__single_night_fee = value

    def save_data(self) -> None:
        try:
            data = {
                "total_slots": self.__total_slots,
                "monthly_fee": self.__monthly_fee,
                "single_day_fee": self.__single_day_fee,
                "single_night_fee": self.__single_night_fee,
            }

            with open(self.__settings_file, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            raise Exception(e) from e

    def eq_monthly_fee(self, monthly_fee: int) -> bool:
        return self.__monthly_fee == monthly_fee

    def eq_single_day_fee(self, single_day_fee: int) -> bool:
        return self.__single_day_fee == single_day_fee

    def eq_single_night_fee(self, single_night_fee: int) -> bool:
        return self.__single_night_fee == single_night_fee
