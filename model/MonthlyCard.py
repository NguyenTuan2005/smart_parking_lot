from datetime import date
from model.Card import Card
from model.Customer import Customer
from model.Vehicle import Vehicle


class MonthlyCard(Card):
    def __init__(self, card_id: str, fee: int, start_date: date, expiry_date: date, customer: Customer,
                 vehicle: Vehicle, is_paid: bool):
        super().__init__(card_id=card_id,fee=fee,vehicle=vehicle)
        self._start_date = start_date
        self._expiry_date = expiry_date
        self._customer = customer
        self._is_paid = is_paid

    def __repr__(self):
        return (
                super().__repr__() +
                f", start date: {self._start_date.strftime('%d/%m/%Y')}, "
                f"expiry date: {self._expiry_date.strftime('%d/%m/%Y')}"
                f"customer: {self._customer}"
        )

    @property
    def expiry_date(self):
        return self._expiry_date

    def is_valid(self) -> bool:
        return date.today() <= self._expiry_date

    @property
    def customer(self):
        return self._customer

    @property
    def start_date(self):
        return self._start_date

    @property
    def is_paid(self):
        return self._is_paid
