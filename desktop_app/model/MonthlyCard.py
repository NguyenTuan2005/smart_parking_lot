from datetime import datetime, date
from typing import Optional

from desktop_app.model.Card import Card
from desktop_app.model.Customer import Customer
from desktop_app.model.Vehicle import Vehicle


class MonthlyCard(Card):
    def __init__(self, card_id: str, expiry_date: date, is_paid: bool, customer: Customer, vehicle: Optional[Vehicle] = None):
        super().__init__(card_id, datetime.now())
        self._expiry_date = expiry_date
        self._customer = customer
        self._vehicle = vehicle
        self._is_paid = is_paid

    @property
    def expiry_date(self):
        return self._expiry_date

    def is_valid(self) -> bool:
        return date.today() <= self._expiry_date
