from dao.CustomerDAO import CustomerDAO
from dao.MonthlyCardDAO import MonthlyCardDAO
from dao.VehicleDAO import VehicleDAO
from services.CardService import MonthlyCardService


class MonthlyCardController:
    def __init__(self, view):
        self.view = view
        self.monthly_card_service = MonthlyCardService()

        self.view.cardAdded.connect(self.create_monthly_card)
        self.view.deleteRequested.connect(self.handle_delete_card)

        self.load_data()

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
