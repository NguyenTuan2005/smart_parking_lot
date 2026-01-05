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
        self.__day_start = 6
        self.__day_end = 22
        self.__single_day_fee = 3000
        self.__single_night_fee = 5000

        settings_file = Path("settings.json")
        if settings_file.exists():
            with open(settings_file, "r") as file:
                data = json.load(file)
                self.__total_slots = data.get("total_slots", self.__total_slots)
                self.__monthly_fee = data.get("monthly_fee", self.__monthly_fee)
                self.__day_start = data.get("day_start", self.__day_start)
                self.__day_end = data.get("day_end", self.__day_end)
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
    def day_start(self):
        return self.__day_start

    @day_start.setter
    def day_start(self, value: int):
        self.__day_start = value

    @property
    def day_end(self):
        return self.__day_end

    @day_end.setter
    def day_end(self, value: int):
        self.__day_end = value

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
