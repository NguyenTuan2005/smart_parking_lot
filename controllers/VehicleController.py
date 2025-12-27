import hashlib

from PyQt6.QtWidgets import QMessageBox, QDialog
from dao.VehicleDAO import VehicleDAO

from ui.admin.tabs.AddStaffDialog import AddStaffDialog



class VehicleController:
    def __init__(self, view):
        self.view = view
        self.dao = VehicleDAO()

        # load ban đầu
        self.load_data()

        # connect nút
        self.view.btn_edit.clicked.connect(self.edit_staff)
        self.view.btn_delete.clicked.connect(self.delete_staff)
        self.view.btn_add.clicked.connect(self.add_staff )
        self.view.search_btn.clicked.connect(self.search)
        self.view.refresh_btn.clicked.connect(self.load_data)

    def load_data(self):
        try:
            rows = self.dao.get_all()
            self.view.set_table_data(rows)
        except Exception as e:
            print("Lỗi load vehicle:", e)

    def search(self):
        keyword = self.view.search_input.text().strip()

        if not keyword:
            self.load_data()
            return

        try:
            rows = self.dao.search_by_name(keyword)
            self.view.set_table_data(rows)
        except Exception as e:
            print("Lỗi tìm kiếm:", e)

    def insert_staff(self, fullname, phone_number, username, password, role):
        if not all([fullname, phone_number, username, password]):
            print("Thiếu dữ liệu thêm nhân viên")
            return False

        # hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = self._db.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO staffs (fullname, phone_number, username, password, role)
                VALUES (?, ?, ?, ?, ?)
            """, (
                fullname.strip(),
                phone_number.strip(),
                username.strip(),
                hashed_password,
                role
            ))

            conn.commit()
            return True

        except Exception as e:
            print("Lỗi thêm nhân viên:", e)
            conn.rollback()
            return False

        finally:
            cursor.close()

            conn.close()

    def add_staff(self):
        dialog = AddStaffDialog(self.view)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            success = self.dao.insert_staff(
                fullname=data["fullname"],
                phone_number=data["phone"],
                username=data["username"],
                password=data["password"],
                role=data["role"]
            )

            if success:
                QMessageBox.information(self.view, "Thành công", "Đã thêm nhân viên")
                self.load_data()
            else:
                QMessageBox.critical(self.view, "Lỗi", "Thêm nhân viên thất bại")

    def delete_staff(self):
        row = self.view.table.currentRow()

        if row < 0:
            QMessageBox.warning(self.view, "Chưa chọn", "Vui lòng chọn nhân viên cần xóa")
            return

        staff_id = int(self.view.table.item(row, 0).text())
        fullname = self.view.table.item(row, 1).text()

        reply = QMessageBox.question(
            self.view,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa nhân viên '{fullname}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = self.dao.delete_staff(staff_id)

            if success:
                QMessageBox.information(self.view, "Thành công", "Đã xóa nhân viên")
                self.load_data()
            else:
                QMessageBox.critical(self.view, "Lỗi", "Xóa thất bại")

    def edit_staff(self):
        row = self.view.table.currentRow()

        if row < 0:
            QMessageBox.warning(self.view, "Chưa chọn", "Vui lòng chọn nhân viên cần chỉnh sửa")
            return

        staff_id = int(self.view.table.item(row, 0).text())
        fullname = self.view.table.item(row, 1).text()
        phone = self.view.table.item(row, 2).text()
        username = self.view.table.item(row, 3).text()
        role_text = self.view.table.item(row, 4).text()
        role = 1 if role_text == "Admin" else 0

        dialog = AddStaffDialog(self.view)

        # đổ dữ liệu cũ
        dialog.set_data(fullname, phone, username, role)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()

            hashed_password = None
            if data["password"]:
                hashed_password = hashlib.sha256(data["password"].encode()).hexdigest()

            success = self.dao.update_staff(
                staff_id=staff_id,
                fullname=data["fullname"],
                phone=data["phone"],
                username=data["username"],
                password=hashed_password,
                role=data["role"]
            )

            if success:
                QMessageBox.information(self.view, "Thành công", "Đã cập nhật nhân viên")
                self.load_data()
            else:
                QMessageBox.critical(self.view, "Lỗi", "Cập nhật thất bại")
