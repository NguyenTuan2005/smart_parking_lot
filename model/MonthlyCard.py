from datetime import date

from model.Card import Card
from model.Customer import Customer
from model.Vehicle import Vehicle


class MonthlyCard(Card):
    def __init__(
        self,
        card_id: int,
        card_code: str,
        customer: Customer,
        vehicle: Vehicle,
        monthly_fee: int,
        start_date: date,
        expiry_date: date,
        is_paid: bool
    ):
        super().__init__(card_id, card_code)
        self._customer = customer
        self._vehicle = vehicle
        self._monthly_fee = monthly_fee
        self._start_date = start_date
        self._expiry_date = expiry_date
        self._is_paid = is_paid

    def is_valid(self) -> bool:
        return self._is_paid and date.today() <= self._expiry_date

    @property
    def monthly_fee(self) -> int:
        return self._monthly_fee

    @property
    def start_date(self) -> date:
        return self._start_date

    @property
    def expiry_date(self) -> date:
        return self._expiry_date

    @property
    def customer(self) -> Customer:
        return self._customer

    @property
    def vehicle(self) -> Vehicle:
        return self._vehicle

    @property
    def is_paid(self) -> bool:
        return self._is_paid

    def check_in(self, plate: str):
        today =date.today()
        if today > self._expiry_date or not self._is_paid:
            raise Exception("Monthly card is not valid for check-in.")
        return self

    def is_month_card(self):
        return True

    def __repr__(self) -> str:
        return (
            f"MonthlyCard("
            f"id={self.card_id}, "
            f"code='{self.card_code}', "
            f"customer={self._customer}, "
            f"vehicle={self._vehicle}, "
            f"monthly_fee={self._monthly_fee}, "
            f"start_date={self._start_date}, "
            f"expiry_date={self._expiry_date}, "
            f"is_paid={self._is_paid}"
            f")\n"
        )


