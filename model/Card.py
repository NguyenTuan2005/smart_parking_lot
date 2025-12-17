from abc import ABC
from model.CardLog import CardLog

class Card(ABC):
    def __init__(self, card_id: int, card_code: str, card_log: CardLog =None):
        self._card_id = card_id
        self._card_code = card_code
        self._card_log = card_log

    def setCardLog(self, card_log: CardLog):
        self._card_log = card_log

    @property
    def card_log(self) -> CardLog:
        return self._card_log

    @property
    def card_id(self) -> int:
        return self._card_id

    @property
    def card_code(self) -> str:
        return self._card_code

    def __repr__(self):
        return f'{self.__class__.__name__}({self._card_id}, {self._card_code})'


    def calculate_fee(self):
        return self.duration() * 1000


    def duration(self) -> int:
        return self._card_log.duration()

    def check_in(self, plate: str):
        self._card_log.check_in(plate)
        return self

    def is_month_card(self):
        return False