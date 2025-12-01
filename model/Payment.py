from datetime import datetime
from model.Card import Card

class Payment:
    def __init__(self, payment_id: str, card: Card, amount: float, method: str, paid_at: datetime):
        self._id = payment_id
        self._card = card
        self._amount = amount
        self._method = method
        self._paid_at = paid_at

    @property
    def id(self):
        return self._id

    @property
    def method(self):
        return self._method

    @property
    def paid_at(self):
        return self._paid_at

    @property
    def amount(self):
        return self._amount

    @property
    def card(self):
        return self._card

    @amount.setter
    def amount(self, value: float):
        if value < 0:
            raise ValueError("Số tiền không thể âm")
        self._amount = value

    def __repr__(self):
        return "id: " + str(self._id) + " , card: " + str(self._card) + " , amount: " + str(self._amount) + " , method: " + str(self._method) + " , paid at: " + str(self._paid_at)
