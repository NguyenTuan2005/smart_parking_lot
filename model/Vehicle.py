class Vehicle:
    def __init__(self, vehicle_id: int,vehicle_type: str, plate_number: str):
        self.__vehicle_id = vehicle_id
        self.__vehicle_type = vehicle_type
        self.__plate_number = plate_number

    @property
    def vehicle_id(self):
        return self.__vehicle_id

    @property
    def plate_number(self):
        return self.__plate_number

    def __repr__(self):
        return "id: " + str(self.__vehicle_id) + " , plate_number: " + str(self.__plate_number)

    def method(self, type):
        pass