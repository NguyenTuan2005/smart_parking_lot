from desktop_app.model.User import User

class Staff(User):
    def __init__(self, user_id: int, fullname: str, phone_number: str, password: str, role: int):
        super().__init__(user_id, fullname, phone_number)
        self._password = password
        self._role = role

    def check_password(self, password: str) -> bool:
        return self._password == password