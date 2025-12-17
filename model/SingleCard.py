import math

from model.Card import Card
from services.Session import Session


class SingleCard(Card):
    def __init__(self, card_id: int, card_code: str, price: int):
        super().__init__(card_id, card_code)
        self._price = price

    @property
    def price(self) -> int:
        return self._price

    def calculate_price(self, minutes: int) -> int:
        hours = math.ceil(minutes / 60)
        return hours * self._price

    def __repr__(self) -> str:
        return (
            f"SingleCard("
            f"id={self.card_id}, "
            f"code='{self.card_code}', "
            f"price={self._price}"
            f")"
        )

    def check_in(self, plate: str):
        super().check_in(plate)

        from dao.SingleCardDAO import SingleCardDAO
        SingleCardDAO().create(self._card_code, self._price, Session.get_user().id)