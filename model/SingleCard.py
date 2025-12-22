import math

from model.Card import Card
from model.CardLog import CardLog
from services.Session import Session


class SingleCard(Card):
    def __init__(self, card_id: int, card_code: str, price: int, card_log: CardLog =None):
        super().__init__(card_id, card_code)
        self._price = price
        self._card_log = card_log

    def set_card_log(self, card_log: CardLog):
        self._card_log = card_log

    @property
    def card_log(self) -> CardLog:
        return self._card_log

    @property
    def price(self) -> int:
        return self._price

    def duration(self) -> int:
        return self._card_log.duration()

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
        self._card_log.check_in(plate)

        from dao.SingleCardDAO import SingleCardDAO
        SingleCardDAO().create(self._card_code, self._price, Session.get_user().id)

        return self
