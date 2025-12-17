class User:
    def __init__(self, id: int | None, fullname: str, phone_number: str):
        self._id = id
        self._fullname = fullname
        self._phone_number = phone_number

    def __repr__(self):
        return "id: " + str(self._id) + " , fullname: " + str(self._fullname) + " , phone_number: " + str(self._phone_number)

    @property
    def fullname(self):
        return self._fullname

    @property
    def phone_number(self):
        return self._phone_number

    @property
    def id(self):
        return self._id

    