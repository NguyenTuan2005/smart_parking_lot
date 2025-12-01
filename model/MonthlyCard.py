from datetime import datetime, date

from model.Card import Card
from model.Customer import Customer


class MonthlyCard(Card):
    def __init__(self, card_id: str,start_date: date, expiry_date: date, customer: 'Customer', is_paid: bool):
        super().__init__(card_id, datetime.now())
        self.__start_date = start_date
        self.__expiry_date = expiry_date
        self.__customer = customer
        self.__is_paid = is_paid

    @property
    def expiry_date(self):
        return self.__expiry_date

    def is_valid(self) -> bool:
        return date.today() <= self.__expiry_date