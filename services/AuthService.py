from dao.StaffDAO import StaffDAO
from model.Staff import Staff
from typing import Optional


class AuthService:
    def __init__(self):
        self.staff_dao = StaffDAO()

    def login(self, username: str, password: str) -> Optional[Staff]:

        staff = self.staff_dao.get_by_username(username)
        if not staff:
            return None

        if not staff.check_password(password):
            return None

        staff.erase_password()
        return staff
