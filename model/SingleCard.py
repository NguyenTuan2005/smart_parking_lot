import math

from model.Card import Card
from model.CardLog import CardLog
from model.Settings import Settings


class SingleCard(Card):
    def __init__(
        self,
        card_id: int,
        card_code: str,
        price: int,
        night_price: int,
        card_log: CardLog = None,
    ):
        super().__init__(card_id, card_code)
        self._price = price
        self.__night_price = night_price
        self._card_log = card_log
        self.__settings = Settings()

    def set_card_log(self, card_log: CardLog):
        self._card_log = card_log

    @property
    def card_log(self) -> CardLog:
        return self._card_log

    @property
    def price(self) -> int:
        return self._price

    @property
    def night_price(self) -> int:
        return self.__night_price

    @property
    def card_code(self) -> str:
        return self._card_code

    def duration(self) -> int:
        return self._card_log.duration()

    def calculate_price(self, minutes: int) -> int:
        hours = math.ceil(minutes / 60)
        result = self._price if self._card_log.in_day_time() else self.__night_price
        if hours > self.__settings.max_parking_hours:
            result *= self.__settings.overtime_fee
        return result

    def is_single_card(self):
        return True

    def has_check_in(self):
        return self._card_log.has_check_in()

    def has_check_out(self):
        return self._card_log.has_check_out()

    def check_in(self, plate: str):
        self._card_log.check_in(plate, self)
        return self

    def check_out(self, plate):
        if not self.has_check_in():
            return None
        self._card_log.check_out(plate, self)
        return self

    def is_same_plate(self, plate: str) -> bool:
        return self._card_log.is_same_plate(plate)

    def __repr__(self) -> str:
        return (
            f"SingleCard("
            f"id={self.card_id}, "
            f"code='{self.card_code}', "
            f"price={self._price}"
            f")"
        )

    def apply_single_day_fee(self, fee: int):
        if fee <= 0:
            raise ValueError("Giá tiền phải lớn hơn 0")
        self._price = fee

        from dao.SingleCardDAO import SingleCardDAO

        SingleCardDAO().update_price(self._card_id, self._price)

    def apply_single_night_fee(self, night_fee: int):
        if night_fee <= 0:
            raise ValueError("Giá tiền phải lớn hơn 0")
        self._price = night_fee

        from dao.SingleCardDAO import SingleCardDAO

        SingleCardDAO().update_night_price(night_fee)
