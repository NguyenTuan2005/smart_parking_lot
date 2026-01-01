import hashlib
from dao.Staff import Staff

class StaffService:
    def __init__(self):
        self.dao = Staff()

    def get_list(self):
        return self.dao.get_all()

    def search(self, keyword):
        return self.dao.search_by_name(keyword)

    def add_staff(self, data):
        # Hash mật khẩu
        hashed_pw = hashlib.sha256(data["password"].encode()).hexdigest()
        return self.dao.insert(data["fullname"], data["phone"], data["username"], hashed_pw, data["role"])

    def update_staff(self, staff_id, data):
        hashed_pw = None
        if data["password"]: # Chỉ hash nếu người dùng nhập mật khẩu mới
            hashed_pw = hashlib.sha256(data["password"].encode()).hexdigest()
        return self.dao.update(staff_id, data["fullname"], data["phone"], data["username"], hashed_pw, data["role"])

    def delete_staff(self, staff_id):
        return self.dao.delete(staff_id)