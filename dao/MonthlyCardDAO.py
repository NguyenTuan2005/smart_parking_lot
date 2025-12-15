from typing import List, Optional

from dao.CustomerDAO import CustomerDAO
from dao.VehicleDAO import VehicleDAO
from db.database import Database
from model.MonthlyCard import MonthlyCard
from model.Vehicle import Vehicle
from model.Customer import Customer


class MonthlyCardDAO:
    def __init__(self, customer_dao: CustomerDAO, vehicle_dao: VehicleDAO):
        self._db = Database()
        self._customer_dao = customer_dao
        self._vehicle_dao = vehicle_dao

    # ---------- READ ----------
    def get_by_id(self, card_id: int) -> MonthlyCard | None:
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
        SELECT *
        FROM monthly_cards
        WHERE id = ? AND is_active = 1
        """

        row = cursor.execute(sql, card_id).fetchone()
        conn.close()

        if not row:
            return None

        return self._map_row_to_monthly_card(row)

    def get_by_code(self, card_code: str) -> MonthlyCard | None:
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
        SELECT *
        FROM monthly_cards
        WHERE card_code = ? AND is_active = 1
        """

        row = cursor.execute(sql, card_code).fetchone()
        conn.close()

        if not row:
            return None

        return self._map_row_to_monthly_card(row)

    def get_all(self) -> list[MonthlyCard]:
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = "SELECT * FROM monthly_cards WHERE is_active = 1"
        rows = cursor.execute(sql).fetchall()
        conn.close()

        return [self._map_row_to_monthly_card(r) for r in rows]

    # ---------- CREATE ----------
    def create(
        self,
        card_code: str,
        customer_id: int,
        vehicle_id: int,
        monthly_fee: int,
        start_date,
        expiry_date,
        is_paid: bool = True
    ):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
        INSERT INTO monthly_cards
        (card_code, customer_id, vehicle_id,
         monthly_fee, start_date, expiry_date, is_paid)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(
            sql,
            card_code,
            customer_id,
            vehicle_id,
            monthly_fee,
            start_date,
            expiry_date,
            is_paid
        )
        conn.commit()
        conn.close()

    # ---------- UPDATE ----------
    def update_payment(self, card_id: int, is_paid: bool):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
        UPDATE monthly_cards
        SET is_paid = ?, updated_at = GETDATE()
        WHERE id = ?
        """

        cursor.execute(sql, is_paid, card_id)
        conn.commit()
        conn.close()

    def extend_expiry(self, card_id: int, new_expiry):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = """
        UPDATE monthly_cards
        SET expiry_date = ?, updated_at = GETDATE()
        WHERE id = ?
        """

        cursor.execute(sql, new_expiry, card_id)
        conn.commit()
        conn.close()

    # ---------- DELETE (soft) ----------
    def deactivate(self, card_id: int):
        conn = self._db.connect()
        cursor = conn.cursor()

        sql = "UPDATE monthly_cards SET is_active = 0 WHERE id = ?"
        cursor.execute(sql, card_id)
        conn.commit()
        conn.close()

   
    def _map_row_to_monthly_card(self, row) -> MonthlyCard:
        customer = self._customer_dao.get_by_id(row.customer_id)
        vehicle = self._vehicle_dao.get_by_id(row.vehicle_id)

        return MonthlyCard(
            card_id=row.id,
            card_code=row.card_code,
            customer=customer,
            vehicle=vehicle,
            monthly_fee=row.monthly_fee,
            start_date=row.start_date,
            expiry_date=row.expiry_date,
            is_paid=row.is_paid
        )

if __name__ == '__main__':
    print(MonthlyCardDAO(CustomerDAO(), VehicleDAO()).get_all())