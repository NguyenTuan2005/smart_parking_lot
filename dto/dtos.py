from datetime import date
from typing import Optional


class CustomerDTO:
    def __init__(self, fullname: str, phone_number: str, email: str):
        self.fullname = fullname
        self.phone_number = phone_number
        self.email = email


class VehicleDTO:
    def __init__(self, vehicle_type: str, plate_number: str):
        self.vehicle_type = vehicle_type
        self.plate_number = plate_number

class MonthlyCardDTO:
    def __init__(self, card_code: str,
        customer_id: int,
        vehicle_id: int,
        monthly_fee: int,
        start_date: date,
        expiry_date: date,
        is_paid: bool):
        self.card_code = card_code
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.monthly_fee = monthly_fee
        self.start_date = start_date
        self.expiry_date = expiry_date
        self.is_paid = is_paid

class CustomerViewDTO:
    def __init__(
        self,
        customer_id: int,
        customer_name: str,
        phone_number: str,
        email: str,
        plate_number: str,
        vehicle_type: str,
        card_status: str,
        notified: bool = False,
        card_id: Optional[int] = None,
        vehicle_id: Optional[int] = None,
        expiry_date: Optional[date] = None
    ):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.email = email
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type
        self.card_status = card_status
        self.notified = notified
        self.card_id = card_id
        self.vehicle_id = vehicle_id
        self.expiry_date = expiry_date

    def __repr__(self):
        return f'CustomerViewDTO({self.customer_id}, {self.customer_name}, {self.phone_number}, {self.card_status})'


class MonthlyCardCreationDTO:
    def __init__(self, 
                 card_code: str, 
                 customer: CustomerDTO, 
                 vehicle: VehicleDTO, 
                 monthly_fee: int, 
                 start_date: date, 
                 expiry_date: date, 
                 is_paid: bool,
                 months: int = 1,
                 card_id: Optional[int] = None,
                 customer_id: Optional[int] = None,
                 vehicle_id: Optional[int] = None):
        self.card_id = card_id
        self.card_code = card_code
        self.customer = customer
        self.customer_id = customer_id
        self.vehicle = vehicle
        self.vehicle_id = vehicle_id
        self.monthly_fee = monthly_fee
        self.start_date = start_date
        self.expiry_date = expiry_date
        self.months = months
        self.is_paid = is_paid

# for send mail service
class ExpiringMonthlyCardCustomerDTO:
    def __init__(self, customer_id, fullname, email, card_code, expiry_date):
        self.customer_id = customer_id
        self.fullname = fullname
        self.email = email
        self.card_code = card_code
        self.expiry_date = expiry_date

    def  __repr__(self):
        return f'ExpiringCardDTO({self.customer_id}, {self.fullname}, {self.email}, {self.card_code}, {self.expiry_date})\n'
