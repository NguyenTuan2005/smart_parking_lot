import random
from typing import Set, Any, cast

from dao.CustomerDAO import CustomerDAO
from dao.MonthlyCardDAO import MonthlyCardDAO
from dao.PaymentDAO import PaymentDAO
from dao.SingleCardDAO import SingleCardDAO
from dao.StaffDAO import StaffDAO
from dao.VehicleDAO import VehicleDAO
from model.Card import Card
from model.Payment import Payment
from model.SingleCard import SingleCard
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
        self.__users: Set[User] = set(CustomerDAO().get_all()) | set(StaffDAO().get_all())
        self.__cards: Set[Card] = set(SingleCardDAO().get_all()) | set(MonthlyCardDAO(CustomerDAO(), VehicleDAO()).get_all())
        self.__vehicles: Set[Vehicle] = set(VehicleDAO().get_all())
        self.__payments: Set[Payment] = set(PaymentDAO().get_all())

    def check_in(self, card: Card, plate: str) -> Card | None:
        if card is None:
            cards = [c for c in self.__cards if c.has_check_out()]
            card = next((c for c in cards if c.is_month_card() and c.is_same_plate(plate)), None)
            if card is None :
                single_cards = [c for c in cards if c.is_single_card()]
                if len(single_cards) == 0:
                    return None
                card = random.choice(single_cards)
        try:
            card.check_in(plate)
        except Exception as e:
            raise Exception(e) from e
        return card

    def check_out(self, card: Card, plate: str) -> Card | None:
        if card is None:
            cards = [c for c in self.__cards if c.has_check_in()]
            card = next((c for c in cards if c.is_same_plate(plate)), None)
            if card is None:
                raise Exception(f"Không tìm thấy ghi nhận biển số {plate} vào bãi xe")
        try:
            card.check_out(plate)
        except Exception as e:
            raise Exception(e) from e
        return card

    def apply_single_day_fee(self, single_day_fee: int):
        cards = [cast(SingleCard,c) for c in self.__cards if c.is_single_card()]
        try:
            for card in cards:
                card.apply_single_day_fee(single_day_fee)
        except ValueError as e:
            raise ValueError(e) from e

    def apply_single_night_fee(self, single_night_fee: int):
        cards = [cast(SingleCard, c) for c in self.__cards if c.is_single_card()]
        try:
            for card in cards:
                card.apply_single_night_fee(single_night_fee)
        except ValueError as e:
            raise ValueError(e) from e