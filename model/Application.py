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
        self._users: Set[User] = CustomerDAO().get_all().append(StaffDAO().get_all())
        self._cards: Set[Card] = SingleCardDAO().get_all().append(MonthlyCardDAO().get_all())
        self._vehicles: Set[Vehicle] = VehicleDAO().get_all()
        self._payments: Set[Payment] = PaymentDAO().get_all()

    def calculate_total_revenue(self):
        pass

    def statistic_revenue_by_month(self):
        pass

    def check_in(self, card_id: str) :
        pass

    def check_out(self, card_id: str) -> None:
        pass

    def detect_plate(self, card: Card) -> None:
        pass