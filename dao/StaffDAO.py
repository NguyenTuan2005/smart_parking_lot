from typing import Set

from db.database import Database
from model.Staff import Staff


class StaffDAO:
    def __init__(self):
        self.__db = Database()

    def get_all(self) -> Set[Staff]:
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM staffs")
        rows = cursor.fetchall()

        return {Staff(row.id, row.fullname, row.phone_number, row.password, row.role) for row in rows}
