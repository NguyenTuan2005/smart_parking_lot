from model.User import User


class Customer(User):
    def __init__(self, id: int, fullname: str, phone_number: str, email: str):
        super().__init__(id, fullname, phone_number)
        self._email = email

    def __repr__(self):
        return super().__repr__() + " , email: " + str(self._email)

    @property
    def fullname(self):
        return self._fullname

    @property
    def email(self):
        return self._email