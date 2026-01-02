from PyQt6.QtWidgets import QMessageBox, QDialog
from services.StaffService import StaffService
from ui.admin.tabs.AddStaffDialog import AddStaffDialog


class StaffCL:
    def __init__(self, view):
        self.view = view
        self.service = StaffService()

        # Connect signals
        self.view.btn_add.clicked.connect(self.handle_add)
        self.view.btn_edit.clicked.connect(self.handle_edit)
        self.view.btn_delete.clicked.connect(self.handle_delete)
        self.view.search_btn.clicked.connect(self.handle_search)
        self.view.refresh_btn.clicked.connect(self.load_data)
        self.load_data()

    def load_data(self):
        rows = self.service.get_list()
        self.view.set_table_data(rows)

    def handle_search(self):
        keyword = self.view.search_input.text().strip()
        rows = self.service.search(keyword)
        self.view.set_table_data(rows)

    def handle_add(self):
        dialog = AddStaffDialog(self.view)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self.service.add_staff(dialog.get_data()):
                QMessageBox.information(self.view, "Thành công", "Đã thêm nhân viên")
                self.load_data()
            else:
                QMessageBox.critical(self.view, "Lỗi", "Không thể thêm nhân viên")

    def handle_edit(self):
        row = self.view.table.currentRow()
        if row < 0:
            return QMessageBox.warning(self.view, "Thông báo", "Vui lòng chọn nhân viên")

        staff_id = int(self.view.table.item(row, 0).text())
        dialog = AddStaffDialog(self.view)

        # Đổ dữ liệu cũ vào dialog
        dialog.set_data(
            fullname=self.view.table.item(row, 1).text(),
            phone=self.view.table.item(row, 2).text(),
            username=self.view.table.item(row, 3).text(),
            role=1 if self.view.table.item(row, 4).text() == "Admin" else 0
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self.service.update_staff(staff_id, dialog.get_data()):
                QMessageBox.information(self.view, "Thành công", "Cập nhật thành công")
                self.load_data()

    def handle_delete(self):
        row = self.view.table.currentRow()
        if row < 0: return

        staff_id = int(self.view.table.item(row, 0).text())
        if QMessageBox.question(self.view, "Xác nhận", "Bạn có chắc chắn muốn xóa?") == QMessageBox.StandardButton.Yes:
            if self.service.delete_staff(staff_id):
                self.load_data()