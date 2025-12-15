from datetime import datetime

from dao.VehicleDAO import VehicleDAO
from model.Vehicle import Vehicle


class Card:
    def __init__(self, card_id: str, card_code: str, time_entry: datetime = None, time_exit: datetime = None, fee: int = 0,
                 vehicle: Vehicle = None):
        self._card_id = card_id
        self._card_code = card_code
        self._time_entry = time_entry
        self._time_exit = time_exit
        self._fee = fee
        self._vehicle = vehicle

    @property
    def card_id(self):
        return self._card_id

    @property
    def card_code(self):
        return self._card_code

    @property
    def fee(self):
        return self._fee

    @property
    def vehicle(self):
        return self._vehicle

    @property
    def time_entry(self):
        return self._time_entry

    @property
    def time_exit(self):
        return self._time_exit

    @property
    def customer(self):
        return None

    def __repr__(self):
        return (
            f"id: {self._card_id}, "
            f"code: {self.card_code}, "
            f"time entry: {self._time_entry}, "
            f"time exit: {self._time_exit}, "
            f"fee: {self._fee}, "
            f"vehicle: {self._vehicle}"
        )


    def calculate_fee(self):
        return self.duration() * 1000

    def update_exit_time(self, exit_time: datetime) -> None:
        self._time_exit = exit_time

    def duration(self) -> int:
        if self._time_exit and self._time_entry:
            return int((self._time_exit - self._time_entry).total_seconds() / 60)
        return 0

    def check_in(self, plate: str):
        self._time_entry = datetime.now()
        self._time_exit = None
        self._fee = 0
        vehicle = VehicleDAO().get_by_plate_number(plate)
        if vehicle is None:
            VehicleDAO().save(Vehicle(0,"xe may", plate))

        self._vehicle = VehicleDAO().get_by_plate_number(plate)

    def is_month_card(self):
        return False
