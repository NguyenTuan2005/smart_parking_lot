from dao.CustomerDAO import CustomerDAO
from db.database import Database
from typing import Set

from model.Card import Card
from model.MonthlyCard import MonthlyCard
from model.SingleCard import SingleCard


class CardDAO:
    def __init__(self):
        self.__db = Database()

    def get_all(self) -> Set[Card]:
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cards')
        rows = cursor.fetchall()
        cards = {SingleCard(row.id, row.entry_time, time_exit=row.exit_time, fee=row.fee, plate_number='') for row in rows}

        cursor.execute('SELECT * FROM monthly_cards')
        rows = cursor.fetchall()
        cards.union({MonthlyCard(row.id, row.start_date, row.end_date, CustomerDAO().get_by_id(row.customer_id), True) for row in rows})
        return cards

if __name__ == '__main__':
    print(CardDAO().get_all())

    def get_by_id(self, id: int) -> Card or None:
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM cards WHERE id = {id}')
        card = cursor.fetchone()
        if card:
            return SingleCard(card.id, card.entry_time, time_exit=card.exit_time, fee=card.fee, plate_number='')
        return None

    def get_monthly_card_by_id(self, id: int) -> Card or None:
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM monthly_cards WHERE id = {id}')
        card = cursor.fetchone()
        if card:
            return MonthlyCard(card.id, card.start_date, card.end_date, CustomerDAO().get_by_id(card.customer_id), True)
        return None