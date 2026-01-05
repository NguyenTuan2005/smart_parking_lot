from datetime import date
from typing import List, Optional

from dao.CustomerDAO import CustomerDAO
from dao.VehicleDAO import VehicleDAO
from dto.dtos import CustomerViewDTO
from model.Customer import Customer
from model.Vehicle import Vehicle


class CustomerService:

    def __init__(self):
        self._customer_dao = CustomerDAO()
        self._vehicle_dao = VehicleDAO()

    def get_all_customers_with_cards(self, is_active: int = 1) -> List[CustomerViewDTO]:
        try:
            rows = self._customer_dao.get_all_customer_views(is_active)

            result = []
            today = date.today()

            for row in rows:
                expiry_date = row[6]
                if expiry_date and expiry_date >= today:
                    card_status = "Còn hạn"
                else:
                    card_status = "Hết hạn"

                dto = CustomerViewDTO(
                    customer_id=row[0],
                    customer_name=row[1],
                    phone_number=row[2] or "",
                    email=row[3] or "",
                    plate_number=row[4] or "",
                    vehicle_type=row[5] or "Xe máy",
                    card_status=card_status,
                    notified=bool(row[7]),
                    card_id=row[8],
                    vehicle_id=row[9],
                    expiry_date=expiry_date,
                )
                result.append(dto)

            return result
        except Exception as e:
            print(f"Error in CustomerService.get_all_customers_with_cards: {e}")
            return []

    def search_customers(
        self, keyword: str, is_active: int = 1
    ) -> List[CustomerViewDTO]:
        try:
            all_customers = self.get_all_customers_with_cards(is_active)
            keyword_lower = keyword.lower()

            filtered = []
            for dto in all_customers:
                if (
                    keyword_lower in dto.customer_name.lower()
                    or keyword_lower in (dto.phone_number or "")
                    or keyword_lower in (dto.plate_number.lower() or "")
                    or keyword_lower in (dto.email.lower() or "")
                ):
                    filtered.append(dto)

            return filtered
        except Exception as e:
            print(f"Error in CustomerService.search_customers: {e}")
            return []

    def lock_customer(self, customer_id: int) -> bool:
        try:
            return self._customer_dao.delete(customer_id)
        except Exception as e:
            print(f"Error in CustomerService.lock_customer: {e}")
            return False

    def unlock_customer(self, customer_id: int) -> bool:
        try:
            return self._customer_dao.unlock(customer_id)
        except Exception as e:
            print(f"Error in CustomerService.unlock_customer: {e}")
            return False

    def update_customer_info(self, customer_view_dto: CustomerViewDTO) -> bool:
        try:
            # Update customer
            customer = Customer(
                id=customer_view_dto.customer_id,
                fullname=customer_view_dto.customer_name,
                phone_number=customer_view_dto.phone_number,
                email=customer_view_dto.email,
            )
            customer_success = self._customer_dao.update(customer)

            # Update vehicle
            vehicle = Vehicle(
                vehicle_id=customer_view_dto.vehicle_id,
                vehicle_type=customer_view_dto.vehicle_type,
                plate_number=customer_view_dto.plate_number,
            )
            vehicle_success = self._vehicle_dao.update(vehicle)

            return customer_success and vehicle_success
        except Exception as e:
            print(f"Error in CustomerService.update_customer_info: {e}")
            return False
