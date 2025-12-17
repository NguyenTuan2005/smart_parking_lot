from typing import List, Optional

from dao.CustomerDAO import CustomerDAO
from dao.VehicleDAO import VehicleDAO
from db.database import Database
from model.MonthlyCard import MonthlyCard
from model.Payment import Payment
from dao.SingleCardDAO import SingleCardDAO
from dao.MonthlyCardDAO import MonthlyCardDAO
from model.SingleCard import SingleCard


class PaymentDAO:
    def __init__(self):
        self._single_card_dao = SingleCardDAO()
        self._monthly_card_dao = MonthlyCardDAO(CustomerDAO(), VehicleDAO())
        self._db = Database()

    def get_all(self) -> List[Payment]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, card_id, monthly_card_id, amount, method, payment_date
                FROM payments
            """)
            rows = cursor.fetchall()
            payments = []
            for row in rows:
                card = None
                if row[1]:
                    card = self._single_card_dao.get_by_id(row[1])
                elif row[2]:
                    card = self._monthly_card_dao.get_by_id(row[2])

                payment = Payment(
                    payment_id=str(row[0]),
                    card=card,
                    amount=row[3],
                    method=row[4],
                    paid_at=row[5]
                )
                payments.append(payment)
            cursor.close()
            conn.close()
            return payments
        except Exception as e:
            print(f"Error retrieving payments: {e}")

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, card_id, monthly_card_id, amount, method, payment_date
            FROM payments
            WHERE id = ?
        """, (payment_id,))

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            card = None
            if row[1]:
                card = self._single_card_dao.get_by_id(row[1])
            elif row[2]:
                card = self._monthly_card_dao.get_by_id(row[2])

            return Payment(
                payment_id=str(row[0]),
                card=card,
                amount=row[3],
                method=row[4],
                paid_at=row[5]
            )
        return None

    def save(self, payment: Payment) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        card_id = payment.card.card_id if isinstance(payment.card, SingleCard) else None
        monthly_card_id = payment.card.card_id if isinstance(payment.card, MonthlyCard) else None

        cursor.execute("""
            INSERT INTO payments (card_id, monthly_card_id, amount, method, payment_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, GETDATE(), GETDATE())
        """, (
            card_id,
            monthly_card_id,
            payment.amount,
            payment.method,
            payment.paid_at
        ))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0

    def update(self, payment: Payment) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        card_id = payment.card.card_id if isinstance(payment.card, SingleCard) else None
        monthly_card_id = payment.card.card_id if isinstance(payment.card, MonthlyCard) else None

        cursor.execute("""
            UPDATE payments
            SET card_id = ?, monthly_card_id = ?, amount = ?, method = ?, payment_date = ?, updated_at = GETDATE()
            WHERE id = ?
        """, (
            card_id,
            monthly_card_id,
            payment.amount,
            payment.method,
            payment.paid_at,
            int(payment.id)
        ))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0

    def delete(self, payment_id: int) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))

        conn.commit()
        result = cursor.rowcount
        cursor.close()
        conn.close()
        return result > 0

if __name__ == '__main__':
    dao = PaymentDAO()
    print(dao.get_all())

