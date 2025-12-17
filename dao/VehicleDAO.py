from typing import List, Optional
from db.database import Database
from dto.dtos import VehicleDTO
from model.Vehicle import Vehicle


class VehicleDAO:
    def __init__(self):
        self._db = Database()

    def get_all(self) -> List[Vehicle]:
        conn = self._db.connect()
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
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, vehicle_type, plate_number
            FROM vehicles
            WHERE id = ?
        """, (vehicle_id,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Vehicle(row[0], row[1], row[2])
        return None

    def get_by_plate(self, plate_number) -> Optional[Vehicle]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, vehicle_type, plate_number
                FROM vehicles
                WHERE plate_number = ?
            """, plate_number)

            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                return Vehicle(row[0], row[1], row[2])
            return None
        except Exception as e:
            print(f"Lỗi DB VehicleDAO.get_by_plate: {e}")
            return None

    def save(self, vehicle_dto: VehicleDTO) -> int | None:
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                           INSERT INTO vehicles (plate_number, vehicle_type)
                           OUTPUT INSERTED.id
                           VALUES (?, ?)
                           """, (vehicle_dto.plate_number, vehicle_dto.vehicle_type))

            last_id = cursor.fetchone()[0]
            conn.commit()
            return last_id

        except Exception as e:
            print(f"Lỗi DB VehicleDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    def update(self, vehicle: Vehicle) -> bool:
        conn = self._db.connect()
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
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM vehicles WHERE id = ?
        """, (vehicle_id,))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0

