from typing import List, Optional
from db.database import Database
from dto.dtos import CustomerDTO, ExpiringMonthlyCardCustomerDTO
from model.Customer import Customer


class CustomerDAO:
    def __init__(self):
        self._db = Database()

    def get_all(self) -> List[Customer]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT id, full_name, phone_number, email
                           FROM customers
                           WHERE is_active = 1
                           """)
            rows = cursor.fetchall()

            customers = [Customer(row[0], row[1], row[2], row[3]) for row in rows]

            cursor.close()
            conn.close()
            return customers
        except Exception as e:
            print(f"Error in CustomerDAO.get_all: {e}")
            return []

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        try:
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
        except Exception as e:
            print(f"Error in CustomerDAO.get_by_id: {e}")
            return None

    def get_by_phone(self, phone_number) -> Optional[Customer]:
        try:
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
        except Exception as e:
            print(f"Error in CustomerDAO.get_by_phone: {e}")
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
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            cursor.execute("""
                           UPDATE customers
                           SET full_name    = ?,
                               phone_number = ?,
                               email        = ?,
                               updated_at   = GETDATE()
                           WHERE id = ?
                           """, (customer.fullname, customer.phone_number, customer.email, customer.id))

            conn.commit()
            result = cursor.rowcount
            cursor.close()
            conn.close()
            return result > 0
        except Exception as e:
            print(f"Error in CustomerDAO.update: {e}")
            return False

    def delete(self, customer_id: int) -> bool:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            cursor.execute("""
                           UPDATE customers
                           SET is_active = 0
                           WHERE id = ?
                           """, (customer_id,))

            conn.commit()
            result = cursor.rowcount
            cursor.close()
            conn.close()
            return result > 0
        except Exception as e:
            print(f"Error in CustomerDAO.delete: {e}")
            return False

    def unlock(self, customer_id: int) -> bool:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            cursor.execute("""
                           UPDATE customers
                           SET is_active = 1
                           WHERE id = ?
                           """, (customer_id,))

            conn.commit()
            result = cursor.rowcount
            cursor.close()
            conn.close()
            return result > 0
        except Exception as e:
            print(f"Error in CustomerDAO.unlock: {e}")
            return False

    def get_all_customer_views(self, is_active: int = 1) -> list:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            
            sql = """
                SELECT 
                    c.id as customer_id,
                    c.full_name,
                    c.phone_number,
                    c.email,
                    v.plate_number,
                    v.vehicle_type,
                    mc.expiry_date,
                    c.notified,
                    mc.id as card_id,
                    v.id as vehicle_id
                FROM monthly_cards mc
                JOIN customers c ON mc.customer_id = c.id
                JOIN vehicles v ON mc.vehicle_id = v.id
                WHERE mc.is_active = 1 AND c.is_active = ?
                ORDER BY c.full_name
            """
            
            rows = cursor.execute(sql, (is_active,)).fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Error in CustomerDAO.get_all_customer_views: {e}")
            return []


    # for email service
    def get_users_expiring_in_days(self, days=3):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            cursor.execute("""
                           SELECT c.id, c.full_name, c.email, m.card_code, m.expiry_date
                           FROM monthly_cards m
                           JOIN customers c ON  m.customer_id = c.id
                           WHERE m.expiry_date BETWEEN CAST(GETDATE() AS DATE)
                               AND DATEADD(DAY, ?, CAST(GETDATE() AS DATE))
                               AND notified = 0
                           """, days)
            rows = cursor.fetchall()

            result = []
            for r in rows:
                result.append(
                    ExpiringMonthlyCardCustomerDTO(
                        customer_id=r.id,
                        fullname=r.full_name,
                        email=r.email,
                        card_code=r.card_code,
                        expiry_date=r.expiry_date
                    )
                )
            return result
        except Exception as e:
            print(f"Error in CustomerDAO.get_users_expiring_in_days: {e}")
            return []

    def mark_notified(self, customer_id):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            cursor.execute("""
                           UPDATE customers
                           SET notified = 1
                           WHERE id = ?
                           """, customer_id)

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error in CustomerDAO.mark_notified: {e}")
