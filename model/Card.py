from datetime import datetime
from model.Vehicle import Vehicle


class Card:
    def __init__(self, card_id: str, time_entry: datetime = None, time_exit: datetime = None, fee: int = 0,
                 vehicle: Vehicle = None):
        self._card_id = card_id
        self._time_entry = time_entry
        self._time_exit = time_exit
        self._fee = fee
        self._vehicle = vehicle

    @property
    def card_id(self):
        return self._card_id

    @property
    def fee(self):
        return self._fee

    @property
    def vehicle(self):
        return self._vehicle

    def __repr__(self):
        return (
            f"id: {self._card_id}, "
            f"time entry: {self._time_entry}, "
            f"time exit: {self._time_exit}, "
            f"fee: {self._fee}, "
            f"vehicle: {self._vehicle}"
        )

    def calculate_fee(self):
        pass

    def update_exit_time(self, exit_time: datetime) -> None:
        self._time_exit = exit_time

    def duration(self) -> int:
        if self._time_exit and self._time_entry:
            return int((self._time_exit - self._time_entry).total_seconds() / 60)
        return 0

    @property
    def time_entry(self):
        return self._time_entry

    @property
    def time_exit(self):
        return self._time_exit
