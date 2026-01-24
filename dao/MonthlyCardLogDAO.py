from db.database import Database
from model.MonthlyCardLog import MonthlyCardLog


class MonthlyCardLogDAO:
    def __init__(self):
        self._db = Database()

    def get_by_monthly_card_id(self, monthly_card_id: int) -> MonthlyCardLog | None:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT TOP 1 *
                  FROM monthly_card_logs
                  WHERE monthly_card_id = ?
                  ORDER BY entry_at DESC
                  """

            row = cursor.execute(sql, monthly_card_id).fetchone()
            conn.close()

            if not row:
                return MonthlyCardLog()

            return self._map_row_to_monthly_card_log(row)
        except Exception as e:
            print(f"Error in MonthlyCardLogDAO.get_by_monthly_card_id: {e}")
            return None

    def _map_row_to_monthly_card_log(self, row) -> MonthlyCardLog:
        return MonthlyCardLog(
            id=row.id,
            entry_at=row.entry_at,
            exit_at=row.exit_at
        )