from datetime import datetime

from model.Card import Card

class SingleCard(Card):
    def __init__(self, card_id: str, time_entry: datetime, plate_number: str, time_exit: datetime = None, fee: int = 0):
        super().__init__(card_id, time_entry, time_exit, fee)
        self.__plate_number = plate_number

    @property
    def plate_number(self):
        return self._plate_number

    def method(self, type):
        pass