from datetime import datetime

from model.Card import Card
from model.Vehicle import Vehicle


class SingleCard(Card):
    def __init__(self, card_id: str, card_code: str, time_entry: datetime, time_exit: datetime, vehicle: Vehicle,
                 fee: int = 0):
        super().__init__(
            card_id=card_id,
            card_code= card_code,
            time_entry=time_entry,
            time_exit=time_exit,
            fee=fee,
            vehicle=vehicle
        )

    def check_in(self, plate: str):
        super().check_in(plate)

        from dao.SingleCardDAO import SingleCardDAO
        SingleCardDAO().save(self,1)