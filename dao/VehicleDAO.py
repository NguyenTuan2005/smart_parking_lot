from typing import Optional
from database.database import Database
from dto.dtos import VehicleDTO
from model.Vehicle import Vehicle


class VehicleDAO:
    def __init__(self):
        self._db = Database()

    # =============================
    # LOAD TẤT CẢ PHƯƠNG TIỆN (XE MÁY)
    # =============================
    def get_all(self):
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * from staffs
        """)

        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

# tìm kiếm nhân viên
    def search_by_name(self, keyword: str):
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
             SELECT *
        FROM  staffs 
        WHERE staffs.fullname LIKE ?
    """, (f"%{keyword}%",))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # =============================
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

    # =============================
    def get_by_plate(self, plate_number) -> Optional[Vehicle]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, vehicle_type, plate_number
            FROM vehicles
            WHERE plate_number = ?
        """, (plate_number,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Vehicle(row[0], row[1], row[2])
        return None

    # =============================
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
            print(f"Lỗi DB VehicleDAO.save: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

    # =============================
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

    # =============================
    def delete_staff(self, staff_id: int) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM staffs WHERE id = ?", (staff_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Lỗi xóa nhân viên:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def insert_staff(self, fullname, phone_number, username, password, role):
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO staffs (fullname, phone_number, username, password, role)
                VALUES (?, ?, ?, ?, ?)
            """, (fullname, phone_number, username, password, role))

            conn.commit()
            return True

        except Exception as e:
            print("Lỗi thêm nhân viên:", e)
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    def update_staff(self, staff_id, fullname, phone, username, password, role):
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            if password:
                cursor.execute("""
                    UPDATE staffs
                    SET fullname = ?, phone_number = ?, username = ?, password = ?, role = ?
                    WHERE id = ?
                """, (fullname, phone, username, password, role, staff_id))
            else:  # không đổi mật khẩu
                cursor.execute("""
                    UPDATE staffs
                    SET fullname = ?, phone_number = ?, username = ?, role = ?
                    WHERE id = ?
                """, (fullname, phone, username, role, staff_id))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            print("Lỗi cập nhật nhân viên:", e)
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
