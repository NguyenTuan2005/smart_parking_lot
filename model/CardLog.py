from datetime import datetime

from dao.VehicleDAO import VehicleDAO
from dto.dtos import VehicleDTO
from model.Card import Card
from model.Vehicle import Vehicle
from services.Session import Session


class CardLog:
    def __init__(self, id: int = -1, vehicle: Vehicle = None, entry_at: datetime | None = None, exit_at: datetime | None = None,
                 fee: int = 0):
        self._id = id
        self._vehicle = vehicle
        self._entry_at = entry_at
        self._exit_at = exit_at
        self._fee = fee

    def close(self, exit_time: datetime, fee: int):
        self._exit_at = exit_time
        self._fee = fee

    @property
    def id(self):
        return self._id

    @property
    def entry_at(self):
        return self._entry_at

    @property
    def exit_at(self):
        return self._exit_at

    @property
    def fee(self):
        return self._fee

    @property
    def vehicle(self):
        return self._vehicle

    def __repr__(self) -> str:
        return (
            f"CardLog("
            f"entry_at='{self._entry_at}', "
            f"exit_at={self._exit_at}, "
            f"fee={self._fee}, "
            f"vehicle={self._vehicle}"
            f")"
        )

    def duration(self):
        if  self._entry_at and self._exit_at:
            return int(( self._exit_at - self._entry_at).total_seconds() / 60)
        return 0

    def has_check_out(self):
        return self._exit_at is not None and self._fee != 0

    def check_in(self, plate: str, card: Card):
        self._entry_at = datetime.now()
        self._exit_at = None
        self._fee = 0
        vehicle = VehicleDAO().get_by_plate(plate)
        if vehicle is None:
            VehicleDAO().save(VehicleDTO("xe may", plate))
        self._vehicle = VehicleDAO().get_by_plate(plate)

        from dao.CardLogDAO import CardLogDAO
        CardLogDAO().create_entry(card.card_id, self.vehicle.vehicle_id, Session.get_user().id)

    def check_out(self, plate: str, card: Card):
        if self._vehicle.is_same_plate(plate):
            from dao.CardLogDAO import CardLogDAO
            CardLogDAO().close_log(self, datetime.now(), card.calculate_price(self.duration()), Session.get_user().id)

    def has_check_in(self):
        return self._exit_at is None and self._fee == 0

    def is_same_plate(self, plate: str) -> bool:
        if self._vehicle is None:
            return False
        return self._vehicle.is_same_plate(plate)

    def in_day_time(self):
        if self._entry_at is None:
            return False
        end_of_entry_day = self._entry_at.replace(hour=22, minute=0, second=0, microsecond=0)
        exit_time = self._exit_at if self._exit_at is not None else datetime.now()
        return exit_time <= end_of_entry_day