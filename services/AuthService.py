from dao.StaffDAO import StaffDAO
from model.Staff import Staff
from typing import Optional


class AuthService:
    def __init__(self):
        self.staff_dao = StaffDAO()

    def login(self, username: str, password: str) -> Optional[Staff]:
        staff = self.staff_dao.get_by_username(username)
        if staff and staff.password == password:
            print("AuthService: login successful")
            return staff
        return None



if __name__ == '__main__':
    auth_service = AuthService()
    staff = auth_service.login("employee", "123")
    if staff:
        print(f"Đăng nhập thành công: {staff.username}, Vai trò: {staff.role}")
    else:
        print("Đăng nhập thất bại")