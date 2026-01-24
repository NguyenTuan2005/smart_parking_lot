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
                  SELECT id, card_code, price, night_price
                  FROM cards
                  WHERE id = ? \
                    AND is_active = 1 \
                  """

            row = cursor.execute(sql, card_id).fetchone()
            conn.close()

            if not row:
                return None

            card_log = self._card_log_dao.get_by_card_id(row.id)

            return SingleCard(
                row.id, row.card_code, row.price, row.night_price, card_log=card_log
            )
        except Exception as e:
            print("Error in get_by_id:", e)

    def get_by_code(self, card_code: str) -> SingleCard | None:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
            SELECT id, card_code, price, night_price
            FROM cards
            WHERE card_code = ? AND is_active = 1
            """

            row = cursor.execute(sql, card_code).fetchone()
            conn.close()

            if not row:
                return None

            card_log = self._card_log_dao.get_by_card_id(row.id)

            return SingleCard(
                card_id=row.id,
                card_code=row.card_code,
                price=row.price,
                night_price=row.night_price,
                card_log=card_log,
            )
        except Exception as e:
            print(f"Error in SingleCardDAO.get_by_code: {e}")
            return None

    def get_all(self) -> list[SingleCard]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT id, card_code, price, night_price
                  FROM cards
                  WHERE is_active = 1 
                  """

            rows = cursor.execute(sql).fetchall()
            conn.close()

            cards: list[SingleCard] = []
            for r in rows:
                card_log = self._card_log_dao.get_by_card_id(r.id)
                cards.append(
                    SingleCard(
                        r.id, r.card_code, r.price, r.night_price, card_log=card_log
                    )
                )

            return cards
        except Exception as e:
            print("Error in get_all:", e)
            return []

    def search_cards(self, keyword: str) -> list[SingleCard]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT id, card_code, price, night_price
                  FROM cards
                  WHERE is_active = 1 
                    AND (card_code LIKE ? OR CAST(price AS NVARCHAR) LIKE ?)
                  """
            kw = f"%{keyword}%"
            rows = cursor.execute(sql, kw, kw).fetchall()
            conn.close()

            cards: list[SingleCard] = []
            for r in rows:
                card_log = self._card_log_dao.get_by_card_id(r.id)
                cards.append(
                    SingleCard(
                        r.id, r.card_code, r.price, r.night_price, card_log=card_log
                    )
                )

            return cards
        except Exception as e:
            print("Error in search_cards:", e)
            return []

    def create(self, card: SingleCard):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  INSERT INTO cards (card_code, price, night_price)
                  VALUES (?, ?, ?)
                  """

            cursor.execute(sql, card.card_code, card.price, card.night_price)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error in SingleCardDAO.create: {e}")

    def update_price(self, card_id: int, price: int):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  UPDATE cards
                  SET price = ?, updated_at = GETDATE()
                  WHERE id = ? 
                  """

            cursor.execute(sql, price, card_id)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error in SingleCardDAO.update_price: {e}")

    def update_night_price(self, card_id: int, night_price: int):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  UPDATE cards
                  SET night_price = ?, updated_at = GETDATE()
                  WHERE id = ? 
                  """

            cursor.execute(sql, night_price, card_id)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error in SingleCardDAO.update_night_price: {e}")

    def delete(self, card_id: int):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = "UPDATE cards SET is_active = 0 WHERE id = ?"
            cursor.execute(sql, card_id)
            result = cursor.rowcount
            conn.commit()
            conn.close()
            return result > 0
        except Exception as e:
            print(f"Error in SingleCardDAO.delete: {e}")
            return False

    def get_last_card_code(self) -> str | None:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            sql = "SELECT TOP 1 card_code FROM cards ORDER BY id DESC"
            row = cursor.execute(sql).fetchone()
            conn.close()
            return row[0] if row else None
        except Exception as e:
            print(f"Error in SingleCardDAO.get_last_card_code: {e}")
            return None
