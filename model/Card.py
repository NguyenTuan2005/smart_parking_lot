from abc import ABC
from datetime import datetime
from model.Vehicle import Vehicle
class Card(ABC):
    def __init__(self, card_id: int, card_code: str):
        self._card_id = card_id
        self._card_code = card_code

    @property
    def card_id(self) -> int:
        return self._card_id

    @property
    def card_code(self) -> str:
        return self._card_code

    def __repr__(self):
        return f'{self.__class__.__name__}({self._card_id}, {self._card_code})'