import math
from datetime import datetime
from model.Card import Card
from model.Staff import Staff


class SingleCard(Card):
    def __init__(self, card_id: int, card_code: str, price: int):
        super().__init__(card_id, card_code)
        self._price_per_hour = price

    @property
    def price_per_hour(self) -> int:
        return self._price_per_hour

    def calculate_price(self, minutes: int) -> int:
        hours = math.ceil(minutes / 60)
        return hours * self._price_per_hour

    def __repr__(self) -> str:
        return (
            f"SingleCard("
            f"id={self.card_id}, "
            f"code='{self.card_code}', "
            f"price_per_hour={self._price_per_hour}"
            f")"
        )



