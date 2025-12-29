from datetime import datetime

from dao.VehicleDAO import VehicleDAO
from dto.dtos import VehicleDTO
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

    def duration(self):
        if  self._entry_at and self._exit_at:
            return int(( self._exit_at - self._entry_at).total_seconds() / 60)
        return 0

    def check_in(self, plate: str, card_id: int):
        self._entry_at = datetime.now()
        self._exit_at = None
        self._fee = 0
        vehicle = VehicleDAO().get_by_plate(plate)
        if vehicle is None:
            VehicleDAO().save(VehicleDTO("xe may", plate))
        self._vehicle = VehicleDAO().get_by_plate(plate)

        from dao.CardLogDAO import CardLogDAO
        CardLogDAO().create_entry(card_id, self.vehicle.vehicle_id, Session.get_user().id)
