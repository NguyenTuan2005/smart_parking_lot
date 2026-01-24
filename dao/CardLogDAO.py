from datetime import datetime

from dao.VehicleDAO import VehicleDAO
from db.database import Database
from model.CardLog import CardLog


class CardLogDAO:
    def __init__(self):
        self._db = Database()
        self._vehicle_dao = VehicleDAO()

    def get_by_card_id(self, card_id: int) -> CardLog | None:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT TOP 1 *
                  FROM card_logs
                  WHERE card_id = ? 
                  ORDER BY entry_at DESC
                  """

            row = cursor.execute(sql, card_id).fetchone()
            conn.close()

            if not row:
                return CardLog()

            return self._map_row_to_card_log(row)
        except Exception as e:
            print(f"Error in CardLogDAO.get_by_card_id: {e}")
            return None

    def get_all(self) -> list[CardLog]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
            SELECT *
            FROM card_logs
            ORDER BY entry_at DESC
            """

            rows = cursor.execute(sql).fetchall()
            conn.close()

            return [self._map_row_to_card_log(r) for r in rows]
        except Exception as e:
            print(f"Error in CardLogDAO.get_all: {e}")
            return []

    # lấy xe đang còn đậu trong bãi
    def get_all_active_parking(self) -> list[CardLog]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
            SELECT *
            FROM card_logs
            WHERE exit_at IS NULL
            ORDER BY entry_at ASC
            """

            rows = cursor.execute(sql).fetchall()
            conn.close()

            return [self._map_row_to_card_log(r) for r in rows]
        except Exception as e:
            print(f"Error in CardLogDAO.get_all_active_parking: {e}")
            return []


    def _map_row_to_card_log(self, row) -> CardLog:
        vehicle = self._vehicle_dao.get_by_id(row.vehicle_id)
        card_log = CardLog(
            id=row.id,
            vehicle=vehicle,
            entry_at=row.entry_at,
            exit_at=row.exit_at,
            fee=row.fee if row.fee else 0
        )
        return  card_log

    def create_entry(self, card_id: int, vehicle_id: int, created_by: int) -> CardLog | None:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  INSERT INTO card_logs (card_id, vehicle_id, created_by)
                  OUTPUT INSERTED.*
                  VALUES (?, ?, ?) \
                  """

            row = cursor.execute(sql, card_id, vehicle_id, created_by).fetchone()
            conn.commit()
            conn.close()

            return self._map_row_to_card_log(row)
        except Exception as e:
            print(f'CardLogDao (Error): {e}')
            return None

    def close_log(self, log: CardLog, exit_time: datetime, fee: int, closed_by: int):
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
            UPDATE card_logs
            SET exit_at = ?, fee = ?, closed_by = ?
            WHERE id = ?
            """

            cursor.execute(sql, exit_time, fee, closed_by, log.id)
            conn.commit()
            conn.close()

            # cập nhật object trong memory
            log.close(exit_time, fee)
        except Exception as e:
            print(f"CardLogDao: Error close log {e}")


    def get_open_log_by_card(self, card_id: int) -> CardLog | None:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT TOP 1 *
                  FROM card_logs
                  WHERE card_id = ? \
                    AND exit_at IS NULL
                  ORDER BY entry_at DESC \
                  """

            row = cursor.execute(sql, card_id).fetchone()
            conn.close()

            if not row:
                return None

            return self._map_row_to_card_log(row)
        except Exception as e:
            print(f"Error in CardLogDAO.get_open_log_by_card: {e}")
            return None


    def get_by_date_range(self, from_date: datetime, to_date: datetime) -> list[CardLog]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
            SELECT *
            FROM card_logs
            WHERE entry_at BETWEEN ? AND ?
            ORDER BY entry_at DESC
            """

            rows = cursor.execute(sql, from_date, to_date).fetchall()
            conn.close()

            return [self._map_row_to_card_log(r) for r in rows]
        except Exception as e:
            print(f"Error in CardLogDAO.get_by_date_range: {e}")
            return []

    def get_all_with_details(self) -> list[dict]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
            SELECT cl.id, cl.entry_at, cl.exit_at, cl.fee, cl.created_by,
                   c.card_code,
                   v.plate_number, v.vehicle_type,
                   s.fullname as staff_name
            FROM card_logs cl
            JOIN cards c ON cl.card_id = c.id
            LEFT JOIN vehicles v ON cl.vehicle_id = v.id
            LEFT JOIN staffs s ON cl.created_by = s.id
            ORDER BY cl.entry_at DESC
            """

            rows = cursor.execute(sql).fetchall()
            conn.close()

            results = []
            for row in rows:
                results.append({
                    'id': row.id,
                    'card_code': row.card_code,
                    'plate_number': row.plate_number,
                    'vehicle_type': row.vehicle_type,
                    'entry_at': row.entry_at,
                    'exit_at': row.exit_at,
                    'fee': row.fee if row.fee else 0,
                    'status': "Đã rời đi" if row.exit_at else "Đang gửi",
                    'created_by': row.created_by,
                    'staff_name': row.staff_name
                })
            return results
        except Exception as e:
            print(f"Error in CardLogDAO.get_all_with_details: {e}")
            return []

    def search_logs(self, keyword: str) -> list[dict]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()
            search_pattern = f"%{keyword}%"

            sql = """
            SELECT cl.id, cl.entry_at, cl.exit_at, cl.fee, cl.created_by,
                   c.card_code,
                   v.plate_number, v.vehicle_type,
                   s.fullname as staff_name
            FROM card_logs cl
            JOIN cards c ON cl.card_id = c.id
            LEFT JOIN vehicles v ON cl.vehicle_id = v.id
            LEFT JOIN staffs s ON cl.created_by = s.id
            WHERE c.card_code LIKE ? OR v.plate_number LIKE ?
            ORDER BY cl.entry_at DESC
            """

            rows = cursor.execute(sql, search_pattern, search_pattern).fetchall()
            conn.close()

            results = []
            for row in rows:
                results.append({
                    'id': row.id,
                    'card_code': row.card_code,
                    'plate_number': row.plate_number,
                    'vehicle_type': row.vehicle_type,
                    'entry_at': row.entry_at,
                    'exit_at': row.exit_at,
                    'fee': row.fee if row.fee else 0,
                    'status': "Đã rời đi" if row.exit_at else "Đang gửi",
                    'created_by': row.created_by,
                    'staff_name': row.staff_name
                })
            return results
        except Exception as e:
            print(f"Error in CardLogDAO.search_logs: {e}")
            return []

