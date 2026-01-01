from db.database import Database

class Staff:
    def __init__(self):
        self._db = Database()

    def get_all(self):
        conn = self._db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, fullname, phone_number, username, password, role FROM staffs")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def search_by_name(self, keyword):
        conn = self._db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, fullname, phone_number, username, password, role FROM staffs WHERE fullname LIKE ?", (f"%{keyword}%",))
        rows = cursor.fetchall()
        conn.close()
        return rows

    def insert(self, fullname, phone, username, hashed_password, role):
        conn = self._db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO staffs (fullname, phone_number, username, password, role)
                VALUES (?, ?, ?, ?, ?)
            """, (fullname, phone, username, hashed_password, role))
            conn.commit()
            return True
        except Exception as e:
            print(f"DAO Insert Error: {e}")
            return False
        finally:
            conn.close()

    def update(self, staff_id, fullname, phone, username, password, role):
        conn = self._db.connect()
        cursor = conn.cursor()
        try:
            if password:
                cursor.execute("""
                    UPDATE staffs SET fullname=?, phone_number=?, username=?, password=?, role=? WHERE id=?
                """, (fullname, phone, username, password, role, staff_id))
            else:
                cursor.execute("""
                    UPDATE staffs SET fullname=?, phone_number=?, username=?, role=? WHERE id=?
                """, (fullname, phone, username, role, staff_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"DAO Update Error: {e}")
            return False
        finally:
            conn.close()

    def delete(self, staff_id):
        conn = self._db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM staffs WHERE id = ?", (staff_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success