from PyQt6.QtWidgets import QMessageBox

from dao.CustomerDAO import CustomerDAO
from dao.MonthlyCardDAO import MonthlyCardDAO
from dao.VehicleDAO import VehicleDAO
from services.CardService import MonthlyCardService, SingleCardService


class MonthlyCardController:
    def __init__(self, view):
        self.view = view
        self.monthly_card_service = MonthlyCardService()

        self.view.cardAdded.connect(self.create_monthly_card)
        self.view.deleteRequested.connect(self.handle_delete_card)
        self.view.editRequested.connect(self.update_card)
        
        # New Connections
        if hasattr(self.view, 'btnRefresh'):
            self.view.btnRefresh.clicked.connect(self.load_data)
        
        if hasattr(self.view, 'btnSearch'):
            self.view.btnSearch.clicked.connect(self.search_cards)
            self.view.txtSearchCardCode.returnPressed.connect(self.search_cards)
            
        self.load_data()

    def search_cards(self):
        try:
            keyword = self.view.txtSearchCardCode.text().strip()
            if not keyword:
                self.load_data()
                return

            cards = self.monthly_card_service.search_monthly_cards(keyword)
            self.view.set_table_data(cards)
        except Exception as e:
            print(f"Lỗi tìm kiếm thẻ tháng: {e}")
            
    def load_data(self):
        try:
            cards = self.monthly_card_service.get_all_cards()
            self.view.set_table_data(cards)
        except Exception as e:
            print(f"Lỗi khi load dữ liệu: {e}")

    def create_monthly_card(self, card_data: dict):
        self.monthly_card_service.create_monthly_card(card_data)
        self.load_data()

    def handle_delete_card(self, delete_data: dict):
        card_code = delete_data.get('card_code')
        if not card_code:
            return

        confirmed = self.view.show_confirmation_dialog(
            "Xác nhận xóa thẻ tháng",
            f"Bạn có chắc chắn muốn xóa thẻ tháng {card_code}? Hành động này không thể hoàn tác."
        )

        if not confirmed:
            return

        try:
            success = self.monthly_card_service.delete_card(card_code)
            if success:
                self.load_data()
            else:
                print(f"Lỗi: Không thể xóa thẻ {card_code} (có thể không tìm thấy hoặc lỗi DB).")

        except Exception as e:
            print(f"Lỗi hệ thống khi xóa thẻ: {e}")

    def update_card(self, card_data: dict):
        try:
            self.monthly_card_service.update_card(card_data)
            QMessageBox.information(
                self.view,
                "Thành công",
                "Cập nhật thẻ tháng thành công"
            )

        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Lỗi",
                str(e)
            )

        self.load_data()


class SingleCardLogController:
    def __init__(self, view):
        self.view = view
        self.single_card_service = SingleCardService()

        # Connect signals
        if hasattr(self.view, 'btnRefresh'):
            self.view.btnRefresh.clicked.connect(self.load_data)
        
        if hasattr(self.view, 'btnSearch'):
            self.view.btnSearch.clicked.connect(self.search_logs)
            self.view.txtSearchCardCode.returnPressed.connect(self.search_logs)
        
        self.load_data()

    def load_data(self):
        try:
            logs = self.single_card_service.get_all_logs()
            self.view.set_table_data(logs)
        except Exception as e:
            print(f"SingleCardLogController Error: {e}")

    def search_logs(self):
        try:
            keyword = self.view.txtSearchCardCode.text().strip()
            if not keyword:
                self.load_data()
                return
            
            logs = self.single_card_service.search_logs(keyword)
            self.view.set_table_data(logs)
        except Exception as e:
            print(f"SingleCardLogController Search Error: {e}")


class SingleCardManagementController:
    def __init__(self, view):
        self.view = view
        self.service = SingleCardService()
        
        self.view.createRequested.connect(self.create_card)
        self.view.updateRequested.connect(self.update_card)
        self.view.deleteRequested.connect(self.delete_card)
        
        # New Connections
        if hasattr(self.view, 'btnRefresh'):
            self.view.btnRefresh.clicked.connect(self.load_data)
        
        if hasattr(self.view, 'btnSearch'):
            self.view.btnSearch.clicked.connect(self.search_cards)
            self.view.txtSearch.returnPressed.connect(self.search_cards)
        
        self.load_data()

    def search_cards(self):
        try:
            keyword = self.view.txtSearch.text().strip()
            if not keyword:
                self.load_data()
                return

            cards = self.service.search_single_cards(keyword)
            self.view.set_table_data(cards)
        except Exception as e:
            print(f"Error searching single cards: {e}")

    def load_data(self):
        try:
            cards = self.service.get_all_cards()
            self.view.set_table_data(cards)
        except Exception as e:
            print(f"SingleCardManagementController Load Error: {e}")

    def create_card(self, data):
        try:
            self.service.create_card(data['card_code'], data['price'])
            self.load_data()
        except Exception as e:
            print(f"Error creating card: {e}")

    def update_card(self, data):
        try:
            self.service.update_card(data['card_id'], data['price'])
            self.load_data()
        except Exception as e:
            print(f"Error updating card: {e}")

    def delete_card(self, card_id):
        try:
            self.service.delete_card(card_id)
            self.load_data()
        except Exception as e:
            print(f"Error deleting card: {e}")


