from db.database import Database


class MonthlyCardLogDAO:
    def __init__(self):
        self._db = Database()