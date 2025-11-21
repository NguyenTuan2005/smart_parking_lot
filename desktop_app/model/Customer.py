from desktop_app.model.User import User

class Customer(User):
    def __init__(self, user_id: int, fullname: str, phone_number: str, email: str):
        super().__init__(user_id, fullname, phone_number)
        self._email = email

    @property
    def email(self):
        return self._email
    
    def __repr__(self) -> str:
        return f"Customer(id={self._id}, fullname={self._fullname}, phone_number={self._phone_number}, email={self._email})"