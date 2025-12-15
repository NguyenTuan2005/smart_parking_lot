from typing import List, Optional
from db.database import Database
from model.Customer import Customer

class CustomerDAO:
    def __init__(self):
        self._db = Database()

    def get_all(self) -> List[Customer]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name, phone_number, email
            FROM customers
        """)
        rows = cursor.fetchall()

        customers = [Customer(row[0], row[1], row[2], row[3]) for row in rows]

        cursor.close()
        conn.close()
        return customers

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name, phone_number, email
            FROM customers
            WHERE id = ?
        """, (customer_id,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Customer(row[0], row[1], row[2], row[3])
        return None

    def save(self, customer: Customer) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO customers (full_name, phone_number, email)
            VALUES (?, ?, ?)
        """, (customer.fullname, customer.phone_number, customer.email))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0

    def update(self, customer: Customer) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE customers
            SET full_name = ?, phone_number = ?, email = ?, updated_at = GETDATE()
            WHERE id = ?
        """, (customer.fullname, customer.phone_number, customer.email, customer.id))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0

    def delete(self, customer_id: int) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM customers
            WHERE id = ?
        """, (customer_id,))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0

    def get_or_create(self, name, phone, email):
        conn = self._db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM customers WHERE phone_number=?", (phone,))
            row = cursor.fetchone()
            if row:
                return type('Customer', (), {'id': row[0], 'fullname': name})()  # fake object đơn giản
            # Nếu chưa có, insert
            cursor.execute(
                "INSERT INTO customers (fullname, phone_number, email) VALUES (?, ?, ?)",
                (name, phone, email)
            )
            conn.commit()
            return type('Customer', (), {'id': cursor.lastrowid, 'fullname': name})()
        finally:
            conn.close()
