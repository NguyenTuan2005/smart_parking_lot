from datetime import date

from dao.CustomerDAO import CustomerDAO
from dao.MonthlyCardDAO import MonthlyCardDAO
from dao.VehicleDAO import VehicleDAO
from dto.dtos import CustomerDTO, VehicleDTO, MonthlyCardDTO


class MonthlyCardService:
    def __init__(self):
        self.customer_dao = CustomerDAO()
        self.vehicle_dao = VehicleDAO()
        self.monthly_card_dao = MonthlyCardDAO(self.customer_dao, self.vehicle_dao)

    def get_all_cards(self):
        return self.monthly_card_dao.get_all()


    def validate_customer(self, data: dict) -> int:

        phone = data['phone_number'].strip()

        customer = self.customer_dao.get_by_phone(phone)

        if customer:
            return customer.id
        else:
            customerDTO = CustomerDTO(data['customer_name'],phone, data['customer_email'])
            new_customer_id = self.customer_dao.save(customerDTO)

            return new_customer_id


    def validate_vehicle(self, data: dict, customer_id: int) -> int:

        plate = data['plate_number'].strip()

        vehicle = self.vehicle_dao.get_by_plate(plate)

        if vehicle:
            return vehicle.vehicle_id
        else:
            vehicleDTO = VehicleDTO(plate, data["vehicle_type"])
            new_vehicle_id = self.vehicle_dao.save(vehicleDTO)

            return new_vehicle_id


    def create_monthly_card(self, card_data: dict) -> bool:

        customer_id = self.validate_customer(card_data)

        vehicle_id = self.validate_vehicle(card_data, customer_id)

        card_dto = MonthlyCardDTO(card_data['card_code'], customer_id, vehicle_id, card_data['monthly_fee'], card_data['start_date'], card_data['expiry_date'], card_data['is_paid'])

        try:
            success = self.monthly_card_dao.save(card_dto)
            return success
        except Exception as e:
            print(f"Service: Lỗi DB khi lưu thẻ: {e}")
            return False


    def delete_card(self, card_code: str) -> bool:
        return self.monthly_card_dao.delete(card_code)