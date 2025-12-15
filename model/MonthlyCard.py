from datetime import date

from model.Card import Card
from model.Customer import Customer
from model.Vehicle import Vehicle


class MonthlyCard(Card):
    def __init__(self, card_id: str, card_code: str, fee: int, start_date: date, expiry_date: date, customer: Customer,
                 vehicle: Vehicle, is_paid: bool):
        super().__init__(card_id=card_id, card_code=card_code, fee=fee,vehicle=vehicle)
        self.__start_date = start_date
        self.__expiry_date = expiry_date
        self.__customer = customer
        self.__is_paid = is_paid

    def __repr__(self):
        return (
                super().__repr__() +
                f", start date: {self.__start_date.strftime('%d/%m/%Y')}, "
                f"expiry date: {self.__expiry_date.strftime('%d/%m/%Y')}"
                f"customer: {self.__customer}"
        )

    @property
    def expiry_date(self):
        return self.__expiry_date

    @property
    def customer(self):
        return self.__customer

    @property
    def start_date(self):
        return self.__start_date

    @property
    def is_paid(self):
        return self.__is_paid

    def is_valid(self) -> bool:
        return date.today() <= self.__expiry_date

    def check_in(self, plate: str):
        super().check_in(plate)

        from dao.MonthlyCardDAO import MonthlyCardDAO
        MonthlyCardDAO().update(self)

    def is_month_card(self):
        return True
