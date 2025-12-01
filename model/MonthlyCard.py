from datetime import datetime, date

from model.Card import Card
from model.Customer import Customer
from model.Vehicle import Vehicle


class MonthlyCard(Card):
    def __init__(self, card_id: str,start_date: date, expiry_date: date, customer: 'Customer', vehicle: 'Vehicle', is_paid: bool):
        super().__init__(card_id, datetime.now())
        self._start_date = start_date
        self._expiry_date = expiry_date
        self._customer = customer
        self._vehicle = vehicle
        self._is_paid = is_paid

    def __repr__(self):
        return super.__repr__() + " start date: " + self._start_date.strftime("%d/%m/%Y") + " expiry date: " + self._expiry_date.strftime("%d/%m/%Y")

    @property
    def expiry_date(self):
        return self._expiry_date

    def is_valid(self) -> bool:
        return date.today() <= self._expiry_date