from PyQt6.QtWidgets import QMessageBox

from dto.dtos import CustomerViewDTO
from services.CustomerService import CustomerService


class CustomerController:
 
    def __init__(self, view):
        self.view = view
        self.customer_service = CustomerService()
        self._viewing_active = True # Current view state: True for Active, False for Locked
        
        self.view.lockRequested.connect(self.handle_lock_customer)
        self.view.unlockRequested.connect(self.handle_unlock_customer)
        self.view.customerUpdated.connect(self.handle_update_customer)
        self.view.refreshRequested.connect(self.load_data)
        
        if hasattr(self.view, 'btnSearch'):
            self.view.btnSearch.clicked.connect(self.search_customers)
        
        if hasattr(self.view, 'txtSearch'):
            self.view.txtSearch.returnPressed.connect(self.search_customers)

        if hasattr(self.view, 'btnNotify'):
            self.view.btnNotify.clicked.connect(self.toggle_locked_view)
        
        self.load_data()


    def load_data(self):
        try:
            is_active_flag = 1 if self._viewing_active else 0
            customers = self.customer_service.get_all_customers_with_cards(is_active_flag)
            self.view.set_table_data(customers, is_locked_view=not self._viewing_active)
        except Exception as e:
            print(f"CustomerController - Error loading data: {e}")

    def toggle_locked_view(self):
        self._viewing_active = not self._viewing_active
        
        # Update button text to reflect the alternative view
        if self._viewing_active:
            self.view.btnNotify.setText("Xem khách hàng bị khóa")
        else:
            self.view.btnNotify.setText("Quay lại danh sách")
            
        self.load_data()

    def search_customers(self):
        try:
            keyword = self.view.txtSearch.text().strip()
            if not keyword:
                self.load_data()
                return
            
            is_active_flag = 1 if self._viewing_active else 0
            customers = self.customer_service.search_customers(keyword, is_active_flag)
            self.view.set_table_data(customers, is_locked_view=not self._viewing_active)
        except Exception as e:
            print(f"CustomerController - Error searching customers: {e}")


    def handle_lock_customer(self, customer_dto: CustomerViewDTO):
        customer_id = customer_dto.customer_id
        customer_name = customer_dto.customer_name
        
        if not customer_id:
            return

        try:
            success = self.customer_service.lock_customer(customer_id)
            if success:
                QMessageBox.information(
                    self.view,
                    "Thành công",
                    f"Đã khóa khách hàng '{customer_name}' thành công!"
                )
                self.load_data()
            else:
                QMessageBox.warning(
                    self.view,
                    "Lỗi",
                    f"Không thể khóa khách hàng '{customer_name}'. Vui lòng thử lại."
                )
        except Exception as e:
            print(f"CustomerController - Error locking customer: {e}")
            QMessageBox.critical(
                self.view,
                "Lỗi hệ thống",
                f"Đã xảy ra lỗi khi khóa khách hàng: {str(e)}"
            )

    def handle_unlock_customer(self, customer_dto: CustomerViewDTO):
        customer_id = customer_dto.customer_id
        customer_name = customer_dto.customer_name
        
        if not customer_id:
            return

        try:
            success = self.customer_service.unlock_customer(customer_id)
            if success:
                QMessageBox.information(
                    self.view,
                    "Thành công",
                    f"Đã mở khóa khách hàng '{customer_name}' thành công!"
                )
                self.load_data()
            else:
                QMessageBox.warning(
                    self.view,
                    "Lỗi",
                    f"Không thể mở khóa khách hàng '{customer_name}'. Vui lòng thử lại."
                )
        except Exception as e:
            print(f"CustomerController - Error unlocking customer: {e}")
            QMessageBox.critical(
                self.view,
                "Lỗi hệ thống",
                f"Đã xảy ra lỗi khi mở khóa khách hàng: {str(e)}"
            )

    def handle_update_customer(self, customer_dto: CustomerViewDTO):
        try:
            success = self.customer_service.update_customer_info(customer_dto)
            if success:
                QMessageBox.information(
                    self.view,
                    "Thành công",
                    f"Đã cập nhật thông tin khách hàng '{customer_dto.customer_name}' thành công!"
                )
                self.load_data()
            else:
                QMessageBox.warning(
                    self.view,
                    "Lỗi",
                    f"Không thể cập nhật thông tin khách hàng. Vui lòng kiểm tra lại."
                )
        except Exception as e:
            print(f"CustomerController - Error updating customer: {e}")
            QMessageBox.critical(
                self.view,
                "Lỗi hệ thống",
                f"Đã xảy ra lỗi khi cập nhật: {str(e)}"
            )

    def handle_edit_customer(self, customer_dto: CustomerViewDTO):
        print(f"CustomerController - Edit customer: {customer_dto}")
