from datetime import datetime

class Card:
    def __init__(self, card_id: str, time_entry: datetime, time_exit: datetime = None, fee: int = 0):
        self._card_id = card_id
        self._time_entry = time_entry
        self._time_exit = time_exit
        self._fee = fee

    @property
    def card_id(self):
        return self._card_id

    @property
    def fee(self):
        return self._fee

    def __repr__(self):
        return "id: " + str(self._card_id) + " , time entry: " + str(self._time_entry) + " , time exit: " + str(self._time_exit) + " , fee: " + str(self._fee)

    def calculate_fee(self):
        pass

    def update_exit_time(self, exit_time: datetime) -> None:
        self._time_exit = exit_time

    def duration(self) -> int:
        if self._time_exit and self._time_entry:
            return int((self._time_exit - self._time_entry).total_seconds() / 60)
        return 0