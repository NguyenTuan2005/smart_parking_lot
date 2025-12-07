from typing import List, Optional
from db.database import Database
from model.Staff import Staff


class StaffDAO:
    def __init__(self):
        self._db = Database()

    def get_all(self) -> List[Staff]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, fullname, phone_number, username, password, role
            FROM staffs
        """)
        rows = cursor.fetchall()

        staffs = [
            Staff(row[0], row[1], row[2], row[3], row[4], row[5])
            for row in rows
        ]

        cursor.close()
        conn.close()
        return staffs


    def get_by_id(self, staff_id: int) -> Optional[Staff]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, fullname, phone_number, username, password, role
            FROM staffs
            WHERE id = ?
        """, (staff_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Staff(row[0], row[1], row[2], row[3], row[4], row[5])
        return None


    def get_by_username(self, username: str) -> Optional[Staff]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, fullname, phone_number, username, password, role
            FROM staffs
            WHERE username = ?
        """, (username,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Staff(row[0], row[1], row[2], row[3], row[4], row[5])
        return None


    def save(self, staff: Staff) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO staffs (fullname, phone_number, username, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (
            staff.fullname,
            staff.phone_number,
            staff.username,
            staff.password,
            staff.role
        ))

        conn.commit()

        result = cursor.rowcount
        cursor.close()
        conn.close()

        return result > 0


    def update(self, staff: Staff) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE staffs
            SET fullname = ?, phone_number = ?,username = ?, password = ?, role = ?, update_at = GETDATE()
            WHERE id = ?
        """, (
            staff.fullname,
            staff.phone_number,
            staff.username,
            staff.password,
            staff.role,
            staff.id
        ))

        conn.commit()

        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0


    def delete(self, staff_id: int) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM staffs WHERE id = ?",
            (staff_id,)
        )

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()

        return result > 0

    
