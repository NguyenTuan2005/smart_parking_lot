from dao.CardLogDAO import CardLogDAO
from db.database import Database
from model.CardLog import CardLog
from model.SingleCard import SingleCard


class SingleCardDAO:
    def __init__(self):
        self._db = Database()
        self._card_log_dao = CardLogDAO()

    def get_by_id(self, card_id: int) -> SingleCard | None:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT id, card_code, price
                  FROM cards
                  WHERE id = ? \
                    AND is_active = 1 \
                  """

            row = cursor.execute(sql, card_id).fetchone()
            conn.close()

            if not row:
                return None

            card_log = self._card_log_dao.get_by_card_id(row.id)
            if card_log is None:
                card_log = CardLog()

            return SingleCard(row.id, row.card_code, row.price, card_log= card_log)
        except Exception as e:
            print("Error in get_by_id:", e)

    def get_by_code(self, card_code: str) -> SingleCard | None:
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
        SELECT id, card_code, price
        FROM cards
        WHERE card_code = ? AND is_active = 1
        """

        row = cursor.execute(sql, card_code).fetchone()
        conn.close()

        if not row:
            return None

        card_log = self._card_log_dao.get_by_card_id(row.id)
        if card_log is None:
            card_log = CardLog()

        return SingleCard(
            card_id=row.vehicle_id,
            card_code=row.card_code,
            price=row.price,
            card_log=card_log
        )

    def get_all(self) -> list[SingleCard]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT id, card_code, price
                  FROM cards
                  WHERE is_active = 1 
                  """

            rows = cursor.execute(sql).fetchall()
            conn.close()

            cards: list[SingleCard] = []
            for r in rows:
                card_log = self._card_log_dao.get_by_card_id(r.id)
                if card_log is None:
                    card_log = CardLog()
                cards.append(SingleCard(r.id, r.card_code, r.price, card_log=card_log))

            return cards
        except Exception as e:
            print("Error in get_all:", e)


    # ---------- CREATE ----------
    def create(self, card_code: str, price: int):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
              INSERT INTO cards (card_code, price)
              VALUES (?, ?, ?) \
              """

        cursor.execute(sql, card_code, price)
        conn.commit()
        conn.close()

    # ---------- UPDATE ----------
    def update_price(self, card_id: int, price: int):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
              UPDATE cards
              SET price      = ?, updated_at = GETDATE()
              WHERE id = ? 
              """

        cursor.execute(sql, price, card_id)
        conn.commit()
        conn.close()

    # ---------- DELETE (soft) ----------
    def delete(self, card_id: int):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = "UPDATE cards SET is_active = 0 WHERE id = ?"
        cursor.execute(sql, card_id)
        result = cursor.rowcount
        conn.commit()
        conn.close()
        return result > 0
