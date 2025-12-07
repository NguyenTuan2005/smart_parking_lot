from typing import List, Optional
from db.database import Database
from model.SingleCard import SingleCard
from model.Vehicle import Vehicle


class SingleCardDAO:
    def __init__(self):
        self._db = Database()

    def get_all(self) -> List[SingleCard]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.entry_at, c.exit_at, c.fee,
                   v.id, v.plate_number, v.vehicle_type
            FROM cards c
            JOIN vehicles v ON c.vehicle_id = v.id
            WHERE c.card_type = 'SINGLE'
        """)

        rows = cursor.fetchall()

        cards = [
            SingleCard(
                card_id=row[0],
                time_entry=row[1],
                time_exit=row[2],
                fee=row[3],
                vehicle=Vehicle(row[4], row[5], row[6])
            )
            for row in rows
        ]

        cursor.close()
        conn.close()
        return cards

    def get_by_id(self, card_id: int) -> Optional[SingleCard]:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT c.id, c.entry_at, c.exit_at, c.fee,
                   v.id, v.plate_number, v.vehicle_type
            FROM cards c
            JOIN vehicles v ON c.vehicle_id = v.id
            WHERE c.id = ? AND c.card_type = 'SINGLE'
        """, (card_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return SingleCard(
                card_id=row[0],
                time_entry=row[1],
                time_exit=row[2],
                fee=row[3],
                vehicle=Vehicle(row[4], row[5], row[6])
            )
        return None

    def save(self, card: SingleCard, created_by: int) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cards (vehicle_id, card_type, entry_at, exit_at, fee, created_by)
            VALUES (?, 'SINGLE', ?, ?, ?, ?)
        """, (
            card.vehicle.id,
            card.time_entry,
            card.time_exit,
            card.fee,
            created_by
        ))

        conn.commit()
        result = cursor.rowcount

        cursor.close()
        conn.close()
        return result > 0

    def update_exit_and_fee(self, card: SingleCard, closed_by: int) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE cards
            SET exit_at = ?, fee = ?, closed_by = ?, updated_at = GETDATE()
            WHERE id = ?
        """, (
            card.time_exit,
            card.fee,
            closed_by,
            card.card_id
        ))

        conn.commit()
        result = cursor.rowcount

        cursor.close()
        conn.close()
        return result > 0

    def delete(self, card_id: int) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        conn.commit()

        result = cursor.rowcount
        cursor.close()
        conn.close()

        return result > 0


if __name__ == '__main__':
    dao = SingleCardDAO()
    print(dao.get_all())