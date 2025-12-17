from model.User import User


class Staff(User):
    def __init__(self, id: int, fullname: str, phone_number: str, username: str, password: str, role: int):
        super().__init__(id, fullname, phone_number)
        self._username = username
        self._password = password
        self._role = role

    def __repr__(self):
        return super().__repr__() + " , username: " + str(self._username) + " , password: " + str(
            self._password) + " , role: " + str(self._role)

    def check_password(self, password: str) -> bool:
        return self._password == password

    @property
    def role(self):
        return self._role

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username
