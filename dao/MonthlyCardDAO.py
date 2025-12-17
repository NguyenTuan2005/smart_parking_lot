from datetime import date
from typing import List, Optional

from dao.CustomerDAO import CustomerDAO
from dao.VehicleDAO import VehicleDAO
from db.database import Database
from dto.dtos import MonthlyCardDTO
from model.MonthlyCard import MonthlyCard


class MonthlyCardDAO:
    def __init__(self, customer_dao: CustomerDAO, vehicle_dao: VehicleDAO):
        self._db = Database()
        self._customer_dao = customer_dao
        self._vehicle_dao = vehicle_dao

    # ---------- READ ----------
    def get_by_id(self, card_id: int) -> MonthlyCard | None:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = """
                  SELECT *
                  FROM monthly_cards
                  WHERE id = ?
                    AND is_active = 1 \
                  """

            row = cursor.execute(sql, card_id).fetchone()
            conn.close()

            if not row:
                return None

            return self._map_row_to_monthly_card(row)
        except Exception as e:
            print(f"Lỗi DB MonthlyCardDAO.get_by_id: {e}")

    def get_by_code(self, card_code: str) -> MonthlyCard | None:
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
              SELECT *
              FROM monthly_cards
              WHERE card_code = ?
                AND is_active = 1 \
              """

        row = cursor.execute(sql, card_code).fetchone()
        conn.close()

        if not row:
            return None

        return self._map_row_to_monthly_card(row)

    def get_all(self) -> list[MonthlyCard]:
        try:
            conn = self._db.connect()
            cursor = conn.cursor()

            sql = "SELECT * FROM monthly_cards WHERE is_active = 1"
            rows = cursor.execute(sql).fetchall()
            conn.close()

            return [self._map_row_to_monthly_card(r) for r in rows]
        except Exception as e:
            print(f"Lỗi DB MonthlyCardDAO.get_all: {e}")


    def save(self, card_dto: MonthlyCardDTO) -> bool:

        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            start_date_str = card_dto.start_date.strftime('%Y-%m-%d')
            expiry_date_str = card_dto.expiry_date.strftime('%Y-%m-%d')

            cursor.execute("""
                           INSERT INTO monthly_cards (card_code, customer_id, vehicle_id, monthly_fee,
                                                      start_date, expiry_date, is_paid)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                           """, (
                               card_dto.card_code,
                               card_dto.customer_id,
                               card_dto.vehicle_id,
                               card_dto.monthly_fee,
                               start_date_str,
                               expiry_date_str,
                               card_dto.is_paid
                           ))
            conn.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Lỗi DB MonthlyCardDAO.insert: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def update_payment(self, card_id: int, is_paid: bool):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
              UPDATE monthly_cards
              SET is_paid    = ?,
                  updated_at = GETDATE()
              WHERE id = ? \
              """

        cursor.execute(sql, is_paid, card_id)
        conn.commit()
        conn.close()

    def update(self, card: MonthlyCard):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
              UPDATE monthly_cards
              SET 
                  monthly_fee = ?,
                  is_paid     = ?,
                  updated_at  = GETDATE()
              WHERE id = ? \
              """

        cursor.execute(sql, card.monthly_fee, card.is_paid, card.card_id)
        conn.commit()
        conn.close()

    def extend_expiry(self, card_id: int, new_expiry):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
              UPDATE monthly_cards
              SET expiry_date = ?,
                  updated_at  = GETDATE()
              WHERE id = ? \
              """

        cursor.execute(sql, new_expiry, card_id)
        conn.commit()
        conn.close()

    def delete(self, card_code:str):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = "UPDATE monthly_cards SET is_active = 0 WHERE card_code = ?"
        cursor.execute(sql, card_code)
        result = cursor.rowcount
        conn.commit()
        conn.close()

        return result>0

    def _map_row_to_monthly_card(self, row) -> MonthlyCard:
        customer = self._customer_dao.get_by_id(row.customer_id)
        vehicle = self._vehicle_dao.get_by_id(row.vehicle_id)

        return MonthlyCard(
            card_id=row.vehicle_id,
            card_code=row.card_code,
            customer=customer,
            vehicle=vehicle,
            monthly_fee=row.monthly_fee,
            start_date=row.start_date,
            expiry_date=row.expiry_date,
            is_paid=row.is_paid
        )


