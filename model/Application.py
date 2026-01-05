import random
from typing import Set, Any

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
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Application, cls).__new__(cls, *args, **kwargs)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self._users: Set[User] = set(CustomerDAO().get_all()) | set(StaffDAO().get_all())
        self._cards: Set[Card] = set(SingleCardDAO().get_all()) | set(MonthlyCardDAO(CustomerDAO(), VehicleDAO()).get_all())
        self._vehicles: Set[Vehicle] = set(VehicleDAO().get_all())
        self._payments: Set[Payment] = set(PaymentDAO().get_all())

    def check_in(self, card: Card, plate: str) -> Card | None:
        if card is None:
            cards = [c for c in self._cards if c.has_check_out()]
            if len([c for c in cards if c.is_single_card()]) == 0:
                return None
            card = random.choice(cards)
        try:
            card.check_in(plate)
        except Exception as e:
            raise Exception(e) from e
        return card

    def check_out(self, card: Card, plate: str) -> Card | None:
        if card is None:
            cards = [c for c in self._cards if c.has_check_in()]
            card = next((c for c in cards if c.is_same_plate(plate)), None)
            if card is None:
                return card
        try:
            card.check_out(plate)
        except Exception as e:
            raise Exception(e) from e
        return card