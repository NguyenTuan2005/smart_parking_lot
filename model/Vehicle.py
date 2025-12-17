class Vehicle:
    def __init__(self, vehicle_id: int, vehicle_type: str, plate_number: str):
        self._vehicle_id = vehicle_id
        self._vehicle_type = vehicle_type
        self._plate_number = plate_number

    @property
    def vehicle_id(self):
        return self._vehicle_id

    @property
    def plate_number(self):
        return self._plate_number

    def __repr__(self):
        return "id: " + str(self._vehicle_id) + ", vehicle type:" + str(self._vehicle_type)+ ", plate_number: " + str(self._plate_number)

    def method(self, type):
        pass