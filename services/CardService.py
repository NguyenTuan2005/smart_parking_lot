from util.CardCodeGenerator import CardCodeGenerator
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
from model.SingleCard import SingleCard


class SingleCardService:
    def __init__(self):
        self._card_log_dao = CardLogDAO()
        self._single_card_dao = SingleCardDAO()
        self._customer_dao = CustomerDAO()
        self._vehicle_dao = VehicleDAO()

    def get_all_logs(self):
        return self._card_log_dao.get_all_with_details()

    def search_logs(self, keyword):
        return self._card_log_dao.search_logs(keyword)

    def get_all_cards(self):
        return self._single_card_dao.get_all()

    def search_single_cards(self, keyword):
        return self._single_card_dao.search_cards(keyword)

    def create_card(self, card_code, price, night_price):
        new_card = SingleCard(
            card_id=0, card_code=card_code, price=price, night_price=night_price
        )
        return self._single_card_dao.create(new_card)

    def update_card(self, card_id, price):
        return self._single_card_dao.update_price(card_id, price)

    def delete_card(self, card_id):
        return self._single_card_dao.delete(card_id)

    def generate_next_single_card_code(self) -> str:
        last_code = self._single_card_dao.get_last_card_code()
        return CardCodeGenerator().generate_next_single_card_code(last_code)


class MonthlyCardService:
    def __init__(self):
        self._customer_dao = CustomerDAO()
        self._vehicle_dao = VehicleDAO()
        self._monthly_card_dao = MonthlyCardDAO(self._customer_dao, self._vehicle_dao)

    def get_all_cards(self):
        return self._monthly_card_dao.get_all()

    def search_monthly_cards(self, keyword):
        return self._monthly_card_dao.search_cards(keyword)

    def get_or_create_customer(self, customer_dto: CustomerDTO) -> Customer:
        phone = customer_dto.phone_number.strip()
        customer = self._customer_dao.get_by_phone(phone)

        if customer:
            return customer

        new_customer_id = self._customer_dao.save(customer_dto)
        return Customer(
            id=new_customer_id,
            fullname=customer_dto.fullname,
            phone_number=customer_dto.phone_number,
            email=customer_dto.email,
        )

    def get_or_create_vehicle(self, vehicle_dto: VehicleDTO) -> Vehicle:
        plate = vehicle_dto.plate_number.strip()
        vehicle = self._vehicle_dao.get_by_plate(plate)

        if vehicle:
            return vehicle

        new_vehicle_id = self._vehicle_dao.save(vehicle_dto)
        return Vehicle(
            vehicle_id=new_vehicle_id,
            vehicle_type=vehicle_dto.vehicle_type,
            plate_number=vehicle_dto.plate_number,
        )

    def create_monthly_card(self, card_data: MonthlyCardCreationDTO) -> bool:
        customer = self.get_or_create_customer(card_data.customer)
        vehicle = self.get_or_create_vehicle(card_data.vehicle)

        new_monthly_card = MonthlyCard(
            card_id=0,
            card_code=card_data.card_code,
            customer=customer,
            vehicle=vehicle,
            monthly_fee=card_data.monthly_fee,
            start_date=card_data.start_date,
            expiry_date=card_data.expiry_date,
            is_paid=card_data.is_paid,
        )

        try:
            success = self._monthly_card_dao.save(new_monthly_card)
            return success
        except Exception as e:
            print(f"Service: Lỗi DB khi lưu thẻ: {e}")
            return False

    def delete_card(self, card_code: str) -> bool:
        return self._monthly_card_dao.delete(card_code)

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
            self._customer_dao.update(customer_to_update)
            self._vehicle_dao.update(vehicle_to_update)
            self._monthly_card_dao.update(monthly_card_to_update)

        except Exception as e:
            print(f"Service: Lỗi DB khi cập nhật thẻ: {e}")

    def generate_next_monthly_card_code(self) -> str:
        last_code = self._monthly_card_dao.get_last_card_code()
        return CardCodeGenerator().generate_next_monthly_card_code(last_code)
