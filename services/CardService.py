from datetime import date

from dao.CardLogDAO import CardLogDAO
from dao.CustomerDAO import CustomerDAO
from dao.MonthlyCardDAO import MonthlyCardDAO
from dao.SingleCardDAO import SingleCardDAO
from dao.VehicleDAO import VehicleDAO
from dto.dtos import CustomerDTO, VehicleDTO, MonthlyCardDTO, MonthlyCardCreationDTO
from model.Customer import Customer
from model.MonthlyCard import MonthlyCard
from model.Vehicle import Vehicle


class SingleCardService:
    def __init__(self):
        self.card_log_dao = CardLogDAO()
        self.single_card_dao = SingleCardDAO()
        self.customer_dao = CustomerDAO()
        self.vehicle_dao = VehicleDAO()

    def get_all_logs(self):
        return self.card_log_dao.get_all_with_details()

    def search_logs(self, keyword):
        return self.card_log_dao.search_logs(keyword)

    def get_all_cards(self):
        return self.single_card_dao.get_all()

    def search_single_cards(self, keyword):
        return self.single_card_dao.search_cards(keyword)

    def create_card(self, card_code, price):
        return self.single_card_dao.create(card_code, price)

    def update_card(self, card_id, price):
        return self.single_card_dao.update_price(card_id, price)

    def delete_card(self, card_id):
        return self.single_card_dao.delete(card_id)

    def generate_next_single_card_code(self) -> str:
        last_code = self.single_card_dao.get_last_card_code()
        if not last_code:
            return "C0001"

        try:
            prefix = "C"
            number_part = last_code[len(prefix) :]
            next_number = int(number_part) + 1
            return f"{prefix}{next_number:04d}"
        except (ValueError, TypeError):
            return "C0001"


class MonthlyCardService:
    def __init__(self):
        self.customer_dao = CustomerDAO()
        self.vehicle_dao = VehicleDAO()
        self.monthly_card_dao = MonthlyCardDAO(self.customer_dao, self.vehicle_dao)

    def get_all_cards(self):
        return self.monthly_card_dao.get_all()

    def search_monthly_cards(self, keyword):
        return self.monthly_card_dao.search_cards(keyword)

    def validate_customer(self, customer_dto: CustomerDTO) -> int:
        phone = customer_dto.phone_number.strip()
        customer = self.customer_dao.get_by_phone(phone)

        if customer:
            return customer.id
        else:
            new_customer_id = self.customer_dao.save(customer_dto)
            return new_customer_id

    def validate_vehicle(self, vehicle_dto: VehicleDTO) -> int:
        plate = vehicle_dto.plate_number.strip()
        vehicle = self.vehicle_dao.get_by_plate(plate)

        if vehicle:
            return vehicle.vehicle_id
        else:
            new_vehicle_id = self.vehicle_dao.save(vehicle_dto)
            return new_vehicle_id

    def create_monthly_card(self, card_data: MonthlyCardCreationDTO) -> bool:
        customer_id = self.validate_customer(card_data.customer)
        vehicle_id = self.validate_vehicle(card_data.vehicle)

        card_dto = MonthlyCardDTO(
            card_data.card_code,
            customer_id,
            vehicle_id,
            card_data.monthly_fee,
            card_data.start_date,
            card_data.expiry_date,
            card_data.is_paid,
        )

        try:
            success = self.monthly_card_dao.save(card_dto)
            return success
        except Exception as e:
            print(f"Service: Lỗi DB khi lưu thẻ: {e}")
            return False

    def delete_card(self, card_code: str) -> bool:
        return self.monthly_card_dao.delete(card_code)

    def update_card(self, card_data: MonthlyCardCreationDTO):
        # Validate
        customer_to_update = Customer(
            card_data.customer_id,
            card_data.customer.fullname,
            card_data.customer.phone_number,
            card_data.customer.email,
        )

        vehicle_to_update = Vehicle(
            card_data.vehicle_id,
            card_data.vehicle.vehicle_type,
            card_data.vehicle.plate_number,
        )

        monthly_card_to_update = MonthlyCard(
            card_data.card_id,
            card_data.card_code,
            customer_to_update,
            vehicle_to_update,
            card_data.monthly_fee,
            card_data.start_date,
            card_data.expiry_date,
            card_data.is_paid,
        )

        try:
            self.customer_dao.update(customer_to_update)
            self.vehicle_dao.update(vehicle_to_update)
            self.monthly_card_dao.update(monthly_card_to_update)

        except Exception as e:
            print(f"Service: Lỗi DB khi cập nhật thẻ: {e}")

    def generate_next_monthly_card_code(self) -> str:
        last_code = self.monthly_card_dao.get_last_card_code()
        if not last_code:
            return "MC0001"

        try:
            prefix = "MC"
            number_part = last_code[len(prefix) :]
            next_number = int(number_part) + 1
            return f"{prefix}{next_number:04d}"
        except (ValueError, TypeError):
            return "MC0001"
