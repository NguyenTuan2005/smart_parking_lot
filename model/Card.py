from abc import ABC

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

    def check_in(self, plate: str):
        pass

    def check_out(self, plate: str):
        pass

    def has_check_out(self):
        pass

    def is_month_card(self):
        return False

    def is_single_card(self):
        return False

    def has_check_in(self):
        pass

    def is_same_plate(self, plate: str) -> bool:
        pass

    def calculate_price(self, minutes: int) -> int:
        pass