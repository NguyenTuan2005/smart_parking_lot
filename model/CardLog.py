from datetime import datetime

from model.Card import Card
from model.Vehicle import Vehicle


class CardLog:
    def __init__(self, id: int, card: Card, vehicle: Vehicle, entry_at: datetime, exit_at: datetime | None = None,
                 fee: int = 0):
        self.id = id
        self.card = card
        self.vehicle = vehicle
        self.entry_at = entry_at
        self.exit_at = exit_at
        self.fee = fee

    def close(self, exit_time: datetime, fee: int):
        self.exit_at = exit_time
        self.fee = fee
