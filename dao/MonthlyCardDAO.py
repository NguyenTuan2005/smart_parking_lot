from typing import List, Optional
from db.database import Database
from model.MonthlyCard import MonthlyCard
from model.Vehicle import Vehicle
from model.Customer import Customer


class MonthlyCardDAO:
    def __init__(self):
        self._db = Database()

    def get_all(self) -> List[MonthlyCard]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mc.id, mc.card_code, mc.fee, mc.start_date, mc.end_date, mc.active,
                   c.id, c.full_name, c.phone_number, c.email,
                   v.id, v.plate_number, v.vehicle_type
            FROM monthly_cards mc
            JOIN customers c ON mc.customer_id = c.id
            JOIN vehicles v ON mc.vehicle_id = v.id
        """)

        rows = cursor.fetchall()

        cards = [
            MonthlyCard(
                card_id=row[0],
                card_code=row[1],
                fee=row[2],
                start_date=row[3],
                expiry_date=row[4],
                is_paid=row[5],
                customer=Customer(row[6], row[7], row[8], row[9]),
                vehicle=Vehicle(row[10], row[11], row[12])
            )
            for row in rows
        ]

        cursor.close()
        conn.close()
        return cards

    def get_by_id(self, card_id: int) -> Optional[MonthlyCard]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mc.id, mc.card_code, mc.fee, mc.start_date, mc.end_date, mc.active,
                   c.id, c.full_name, c.phone_number, c.email,
                   v.id, v.plate_number, v.vehicle_type
            FROM monthly_cards mc
            JOIN customers c ON mc.customer_id = c.id
            JOIN vehicles v ON mc.vehicle_id = v.id
            WHERE mc.id = ?
        """, (card_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return MonthlyCard(
                card_id=row[0],
                card_code=row[1],
                fee=row[2],
                start_date=row[3],
                expiry_date=row[4],
                is_paid=row[5],
                customer=Customer(row[6], row[7], row[8], row[9]),
                vehicle=Vehicle(row[10], row[11], row[12])
            )
        return None

    def save(self, card: MonthlyCard) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO monthly_cards
            (card_code, customer_id, vehicle_id, fee, start_date, end_date, active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            card.card_code,
            card.customer.id,
            card.vehicle.vehicle_id,
            card.fee,
            card.start_date,
            card.expiry_date,
            card.is_paid
        ))

        conn.commit()
        result = cursor.rowcount

        cursor.close()
        conn.close()
        return result > 0

    def update(self, card: MonthlyCard) -> bool:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE monthly_cards
                SET card_code= ?, customer_id = ?, vehicle_id = ?, fee = ?,
                    start_date = ?, end_date = ?, active = ?, updated_at = GETDATE()
                WHERE id = ?
            """, (
                card.card_code,
                card.customer.id,
                card.vehicle.vehicle_id,
                card.fee,
                card.start_date,
                card.expiry_date,
                card.is_paid,
                card.card_id
            ))

            conn.commit()
            result = cursor.rowcount

            cursor.close()
            conn.close()
            return result > 0
        except Exception as e:
            print(e)

    def delete(self, card_id: int) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM monthly_cards WHERE id = ?",
            (card_id,)
        )

        conn.commit()
        result = cursor.rowcount

        cursor.close()
        conn.close()
        return result > 0


if __name__ == '__main__':
    dao = MonthlyCardDAO()
    print(dao.get_by_id(1))

