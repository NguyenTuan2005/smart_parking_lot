from dao.StaffDAO import StaffDAO
from model.Staff import Staff
from typing import Optional
import hashlib
import hmac

class AuthService:
    def __init__(self):
        self.staff_dao = StaffDAO()

    def login(self, username: str, password: str) -> Optional[Staff]:

        staff = self.staff_dao.get_by_username(username)
        if not staff:
            return None

        input_password = hashlib.sha256(password.encode()).hexdigest()

        if hmac.compare_digest(input_password, staff.password):
            return staff

        return None