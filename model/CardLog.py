from datetime import datetime

from dao.VehicleDAO import VehicleDAO
from dto.dtos import VehicleDTO
from model.Vehicle import Vehicle


class CardLog:
    def __init__(self, id: int, vehicle: Vehicle, entry_at: datetime, exit_at: datetime | None = None,
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


    def check_in(self, plate: str):
        self._entry_at = datetime.now()
        self._exit_at = None
        self._fee = 0
        vehicle = VehicleDAO().get_by_plate(plate)
        print(vehicle)
        if vehicle is None:
            VehicleDAO().save(VehicleDTO("xe may", plate))
        self._vehicle = VehicleDAO().get_by_plate(plate)
        print("vehicle after check in", self._vehicle)
