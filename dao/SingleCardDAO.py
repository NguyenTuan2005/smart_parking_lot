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
            SELECT c.id, c.card_code, c.entry_at, c.exit_at, c.fee,
                   v.id, v.plate_number, v.vehicle_type
            FROM cards c
            JOIN vehicles v ON c.vehicle_id = v.id
            WHERE c.card_type = 'SINGLE'
        """)

        rows = cursor.fetchall()

        cards = [
            SingleCard(
                card_id=row[0],
                card_code= row[1],
                time_entry=row[2],
                time_exit=row[3],
                fee=row[4],
                vehicle=Vehicle(row[5], row[6], row[7])
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
            SELECT c.id, c.card_code, c.entry_at, c.exit_at, c.fee,
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
                card_code= row[1],
                time_entry=row[2],
                time_exit=row[3],
                fee=row[4],
                vehicle=Vehicle(row[5], row[6], row[7])
            )
        return None

    def save(self, card: SingleCard, created_by: int) -> bool:
        conn = self._db.connect()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cards (card_code, vehicle_id, card_type, entry_at, exit_at, fee, created_by)
            VALUES (?,?, 'SINGLE', ?, ?, ?, ?)
        """, (
            card.card_code,
            card.vehicle.vehicle_id,
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