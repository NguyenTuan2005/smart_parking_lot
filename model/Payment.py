from datetime import datetime

from model.Card import Card


class Payment:
    def __init__(self, payment_id: str, card: Card, amount: float, method: str, paid_at: datetime):
        self.__id = payment_id
        self.__card = card
        self.__amount = amount
        self.__method = method
        self.__paid_at = paid_at

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value: float):
        if value < 0:
            raise ValueError("Số tiền không thể âm")
        self.__amount = value

    def __repr__(self):
        return "id: " + str(self.__id) + " , card: " + str(self.__card) + " , amount: " + str(self.__amount) + " , method: " + str(self.__method) + " , paid at: " + str(self.__paid_at)