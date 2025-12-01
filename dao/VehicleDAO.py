from typing import List, Optional
from db.database import Database
from model.Vehicle import Vehicle


class VehicleDAO:
    def __init__(self):
        self.__db = Database()

    def get_all(self) -> List[Vehicle]:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, plate_number
            FROM vehicles
        """)
        rows = cursor.fetchall()

        vehicles = [Vehicle(row[0], 'xe máy', row[1]) for row in rows]

        cursor.close()
        conn.close()
        return vehicles

    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, plate_number
            FROM vehicles
            WHERE id = ?
        """, (vehicle_id,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Vehicle(row[0], row[1])
        return None

    def save(self, vehicle: Vehicle) -> bool:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO vehicles (plate_number, created_at, updated_at)
            VALUES (?, GETDATE(), GETDATE())
        """, (vehicle.plate_number,))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0

    def update(self, vehicle: Vehicle) -> bool:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE vehicles
            SET plate_number = ?, updated_at = GETDATE()
            WHERE id = ?
        """, (vehicle.plate_number, vehicle.vehicle_id))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0

    def delete(self, vehicle_id: int) -> bool:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM vehicles WHERE id = ?
        """, (vehicle_id,))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0
