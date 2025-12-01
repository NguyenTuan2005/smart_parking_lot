from model.User import User
from model.Vehicle import Vehicle

class Customer(User):
    def __init__(self, user_id: str, fullname: str, phone_number: str, email: str, vehicle: Vehicle = None):
        super().__init__(user_id, fullname, phone_number)
        self.__email = email
        self.__vehicle = vehicle

    def __repr__(self):
        return super().__repr__() + " , email: " + str(self.__email) + " , vehicle: " + str(self.__vehicle)

    @property
    def email(self):
        return self.__email