from typing import List, Optional
from db.database import Database
from dto.dtos import CustomerDTO
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

    def get_by_phone(self, phone_number) -> Optional[Customer]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, full_name, phone_number, email
            FROM customers
            WHERE phone_number = ?
        """, phone_number)

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            return Customer(row[0], row[1], row[2], row[3])
        return None

    def save(self, customer_dto: CustomerDTO) -> int | None:
        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                           INSERT INTO customers (full_name, phone_number, email)
                           OUTPUT INSERTED.id
                           VALUES (?, ?, ?)
                           """, (customer_dto.fullname, customer_dto.phone_number, customer_dto.email))

            last_id = cursor.fetchone()[0]
            conn.commit()

            return last_id

        except Exception as e:
            print(f"Lỗi DB CustomerDAO.create: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()

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


if __name__ == '__main__':
    dao = CustomerDAO()
    dto = CustomerDTO("HHHAA","11123", "hehe@gmail.com")
    print(dao.save(dto))