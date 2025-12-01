from model.User import User

class Staff(User):
    def __init__(self, user_id: str, fullname: str, phone_number: str, password: str, role: int):
        super().__init__(user_id, fullname, phone_number)
        self.__password = password
        self.__role = role

    def __repr__(self):
        return super().__repr__() + " , password: " + str(self.__password) + " , role: " + str(self.__role)

    def check_password(self, password: str) -> bool:
        return self.__password == password