import random
from typing import Set

from dao.CustomerDAO import CustomerDAO
from dao.MonthlyCardDAO import MonthlyCardDAO
from dao.PaymentDAO import PaymentDAO
from dao.SingleCardDAO import SingleCardDAO
from dao.StaffDAO import StaffDAO
from dao.VehicleDAO import VehicleDAO
from model.Card import Card
from model.Payment import Payment
from model.User import User
from model.Vehicle import Vehicle


class Application:
    def __init__(self):
        self._users: Set[User] = set(CustomerDAO().get_all()) | set(StaffDAO().get_all())
        self._cards: Set[Card] = set(SingleCardDAO().get_all()) | set(MonthlyCardDAO(CustomerDAO(), VehicleDAO()).get_all())
        self._vehicles: Set[Vehicle] = set(VehicleDAO().get_all())
        self._payments: Set[Payment] = set(PaymentDAO().get_all())

    def calculate_total_revenue(self):
        pass

    def statistic_revenue_by_month(self):
        pass

    def check_in(self, card: Card, plate: str) -> Card:
        if card is None:
            card = random.choice(list(self._cards))
        card.check_in(plate)
        return card

    def check_out(self, card_id: str) -> None:
        pass

    def detect_plate(self, card: Card) -> None:
        pass