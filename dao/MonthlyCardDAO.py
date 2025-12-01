import pyodbc
from datetime import date, datetime
from typing import List, Optional
from model import MonthlyCard, Customer, Vehicle  # giả sử bạn đã có các lớp này
from dao.CustomerDAO import CustomerDAO
from dao.VehicleDAO import VehicleDAO

class MonthlyCardDAO:
    def __init__(self, connection_string: str):
        self.conn = pyodbc.connect(connection_string)
        self.customer_dao = CustomerDAO(connection_string)
        self.vehicle_dao = VehicleDAO(connection_string)

    def create(self, card: MonthlyCard, price: int) -> int:
        sql = """
        INSERT INTO monthly_cards (customer_id, vehicle_id, price, start_date, end_date, active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, GETDATE(), GETDATE());
        SELECT SCOPE_IDENTITY();
        """
        cursor = self.conn.cursor()
        cursor.execute(
            sql,
            card._customer.id if card._customer else None,
            card._vehicle.id,
            price,
            card._start_date,
            card._expiry_date,
            int(card._is_paid)
        )
        new_id = cursor.fetchval()
        self.conn.commit()
        return new_id

    def get_by_id(self, card_id: int) -> Optional[MonthlyCard]:
        sql = "SELECT * FROM monthly_cards WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, card_id)
        row = cursor.fetchone()
        if row:
            customer = self.customer_dao.get_by_id(row.customer_id) if row.customer_id else None
            vehicle = self.vehicle_dao.get_by_id(row.vehicle_id)
            card = MonthlyCard(
                card_id=str(row.id),
                start_date=row.start_date,
                expiry_date=row.end_date,
                customer=customer,
                vehicle=vehicle,
                is_paid=bool(row.active)
            )
            return card
        return None

    def update(self, card: MonthlyCard, price: int):
        sql = """
        UPDATE monthly_cards
        SET customer_id = ?, vehicle_id = ?, price = ?, start_date = ?, end_date = ?, active = ?, updated_at = GETDATE()
        WHERE id = ?
        """
        cursor = self.conn.cursor()
        cursor.execute(
            sql,
            card._customer.id if card._customer else None,
            card._vehicle.id,
            price,
            card._start_date,
            card._expiry_date,
            int(card._is_paid),
            int(card._card_id)
        )
        self.conn.commit()

    def delete(self, card_id: int):
        sql = "DELETE FROM monthly_cards WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(sql, card_id)
        self.conn.commit()

    def list_all(self) -> List[MonthlyCard]:
        sql = "SELECT * FROM monthly_cards"
        cursor = self.conn.cursor()
        cursor.execute(sql)
        cards = []
        for row in cursor.fetchall():
            customer = self.customer_dao.get_by_id(row.customer_id) if row.customer_id else None
            vehicle = self.vehicle_dao.get_by_id(row.vehicle_id)
            card = MonthlyCard(
                card_id=str(row.id),
                start_date=row.start_date,
                expiry_date=row.end_date,
                customer=customer,
                vehicle=vehicle,
                is_paid=bool(row.active)
            )
            cards.append(card)
        return cards
