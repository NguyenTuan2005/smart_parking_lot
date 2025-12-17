from datetime import datetime

from dao.SingleCardDAO import SingleCardDAO
from dao.VehicleDAO import VehicleDAO
from db.database import Database
from model.CardLog import CardLog


class CardLogDAO:
    def __init__(self, single_card_dao: SingleCardDAO, vehicle_dao: VehicleDAO):
        self._db = Database()
        self._single_card_dao = single_card_dao
        self._vehicle_dao = vehicle_dao

    def get_all(self) -> list[CardLog]:
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

    # lấy xe đang còn đậu trong bãi
    def get_all_active_parking(self) -> list[CardLog]:
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


    def _map_row_to_card_log(self, row) -> CardLog:
        card = self._single_card_dao.get_by_id(row.card_id)
        vehicle = self._vehicle_dao.get_by_id(row.vehicle_id)
        card_log = CardLog(
            id=row.vehicle_id,
            vehicle=vehicle,
            entry_at=row.entry_at,
            exit_at=row.exit_at,
            fee=row.fee if row.fee else 0
        )
        card.setCardLog(card_log)
        return  card_log

    def create_entry(self, card_id: int, vehicle_id: int, created_by: int) -> CardLog:
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

    def close_log(self, log: CardLog, exit_time: datetime, fee: int, closed_by: int):
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


    def get_open_log_by_card(self, card_id: int) -> CardLog | None:
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


    def get_by_date_range(self, from_date: datetime, to_date: datetime) -> list[CardLog]:
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

