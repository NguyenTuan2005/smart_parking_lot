from datetime import date


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