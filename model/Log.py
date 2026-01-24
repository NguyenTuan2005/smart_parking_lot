from abc import ABC
from datetime import datetime


class Log(ABC):
    def __init__(self, id: int = -1, entry_at: datetime | None = None, exit_at: datetime | None = None):
        self._id = id
        self._entry_at = entry_at
        self._exit_at = exit_at

    @property
    def id(self):
        return self._id

    @property
    def entry_at(self):
        return self._entry_at

    @property
    def exit_at(self):
        return self._exit_at

    def has_check_out(self):
        return self._exit_at is not None

    def has_check_in(self):
        return self._exit_at is None

    def duration(self):
        if  self._entry_at and self._exit_at:
            return int(( self._exit_at - self._entry_at).total_seconds() / 60 / 60)
        return 0