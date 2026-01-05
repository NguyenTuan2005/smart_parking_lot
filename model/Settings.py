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
        self.__max_parking_hours = 14
        self.__overtime_fee = 40
        self.__camera_refresh_rate = 100
        self.__ai_cleanup_time = 10

        self.__settings_file = Path("settings.json")
        if self.__settings_file.exists():
            with open(self.__settings_file, "r") as file:
                data = json.load(file)
                self.__total_slots = data.get("total_slots", self.__total_slots)
                self.__monthly_fee = data.get("monthly_fee", self.__monthly_fee)
                self.__single_day_fee = data.get("single_day_fee", self.__single_day_fee)
                self.__single_night_fee = data.get("single_night_fee", self.__single_night_fee)
                self.__max_parking_hours = data.get("max_parking_hours", self.__max_parking_hours)
                self.__overtime_fee = data.get("overtime_fee", self.__overtime_fee)
                self.__camera_refresh_rate = data.get("camera_refresh_rate", self.__camera_refresh_rate)
                self.__ai_cleanup_time = data.get("ai_cleanup_time", self.__ai_cleanup_time)

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

    @property
    def max_parking_hours(self):
        return self.__max_parking_hours

    @max_parking_hours.setter
    def max_parking_hours(self, value: int):
        self.__max_parking_hours = value

    @property
    def overtime_fee(self):
        return self.__overtime_fee

    @overtime_fee.setter
    def overtime_fee(self, value: int):
        self.__overtime_fee = value

    @property
    def camera_refresh_rate(self):
        return self.__camera_refresh_rate

    @camera_refresh_rate.setter
    def camera_refresh_rate(self, value: int):
        self.__camera_refresh_rate = value

    @property
    def ai_cleanup_time(self):
        return self.__ai_cleanup_time

    @ai_cleanup_time.setter
    def ai_cleanup_time(self, value: int):
        self.__ai_cleanup_time = value

    def save_data(self) -> None:
        try:
            data = {
                "total_slots": self.__total_slots,
                "monthly_fee": self.__monthly_fee,
                "single_day_fee": self.__single_day_fee,
                "single_night_fee": self.__single_night_fee,
                "max_parking_hours": self.__max_parking_hours,
                "overtime_fee": self.__overtime_fee,
                "camera_refresh_rate": self.__camera_refresh_rate,
                "ai_cleanup_time": self.__ai_cleanup_time
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
