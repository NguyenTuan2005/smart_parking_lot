class User:
    def __init__(self, user_id: int, fullname: str, phone_number: str):
        self._id = user_id
        self._fullname = fullname
        self._phone_number = phone_number

    def __repr__(self):
        return "id: " + str(self._id) + " , fullname: " + str(self._fullname) + " , phone_number: " + str(self._phone_number)

    @property
    def fullname(self):
        return self._fullname
    
    def __repr__(self) -> str:
        return f"User(id={self._id}, fullname={self._fullname}, phone_number={self._phone_number})"

    