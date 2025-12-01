from typing import Set

from db.database import Database
from model.Vehicle import Vehicle


class VehicleDAO:
    def __init__(self):
        self.__db = Database()

    def get_all(self) -> Set[Vehicle]:
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM vehicles')
        rows = cursor.fetchall()

        return {Vehicle(row.id,
                        row.plate_number) for row in rows}