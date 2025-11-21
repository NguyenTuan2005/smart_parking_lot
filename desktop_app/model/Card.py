from datetime import datetime
from typing import Optional

class Card:
    def __init__(self, card_id: str, time_entry: datetime, status: str = "active", time_exit: Optional[datetime] = None):
        self._card_id = card_id
        self._time_entry = time_entry
        self._time_exit = time_exit
        self._status = status

    @property
    def card_id(self):
        return self._card_id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in ["active", "expired", "closed"]:
            raise ValueError("Trạng thái không hợp lệ")
        self._status = value

    def __repr__(self):
        return "id: " + str(self._card_id) + " , time entry: " + str(self._time_entry) + " , time exit: " + str(self._time_exit) + " , status: " + str(self._status)

    def calculate_fee(self):
        pass

    def update_exit_time(self, exit_time: datetime) -> None:
        self._time_exit = exit_time

    def duration(self) -> int:
        if self._time_exit and self._time_entry:
            return int((self._time_exit - self._time_entry).total_seconds() / 60)
        return 0