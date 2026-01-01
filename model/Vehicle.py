class Vehicle:
    def __init__(self, vehicle_id: int, vehicle_type: str, plate_number: str):
        self._vehicle_id = vehicle_id
        self._vehicle_type = vehicle_type
        self._plate_number = plate_number

    @property
    def vehicle_id(self):
        return self._vehicle_id

    @property
    def vehicle_type(self):
        return self._vehicle_type

    @property
    def plate_number(self):
        return self._plate_number

    def is_same_plate(self, plate: str) -> bool:
        return self._plate_number == plate

    def __repr__(self):
        return "id: " + str(self._vehicle_id) + ", vehicle type:" + str(self._vehicle_type)+ ", plate_number: " + str(self._plate_number)

    def __eq__(self, other):
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self._plate_number == other._plate_number

    def __hash__(self):
        return hash(self._plate_number)