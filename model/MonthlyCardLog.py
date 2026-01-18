from datetime import datetime

from model.Log import Log


class MonthlyCardLog(Log):
    def __init__(self, id: int = -1, entry_at: datetime | None = None, exit_at: datetime | None = None):
        super().__init__(id, entry_at, exit_at)

    def __repr__(self) -> str:
        return (
            f"MonthlyCardLog("
            f"entry_at='{self._entry_at}', "
            f"exit_at={self._exit_at}, "
            f")"
        )