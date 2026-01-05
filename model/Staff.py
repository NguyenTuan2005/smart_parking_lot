from model.User import User
import hashlib
import hmac


class Staff(User):
    def __init__(
        self,
        id: int,
        fullname: str,
        phone_number: str,
        username: str,
        password: str,
        role: int,
    ):
        super().__init__(id, fullname, phone_number)
        self._username = username
        self._password = password
        self._role = role

    def __repr__(self):
        return (
            super().__repr__()
            + " , username: "
            + str(self._username)
            + " , password: "
            + str(self._password)
            + " , role: "
            + str(self._role)
        )

    def check_password(self, input_password: str) -> bool:
        hashed = hashlib.sha256(input_password.encode()).hexdigest()
        return hmac.compare_digest(hashed, self._password)

    def erase_password(self):
        self._password = ""

    @property
    def role(self):
        return self._role

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username
