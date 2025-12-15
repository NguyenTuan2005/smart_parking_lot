class MonthlyCardService:
    def __init__(self, customer_dao, vehicle_dao, monthly_card_dao):
        self.customer_dao = customer_dao
        self.vehicle_dao = vehicle_dao
        self.monthly_card_dao = monthly_card_dao

    def add_monthly_card(self, card_data: dict):
        customer = self.customer_dao.get_or_create(
            name=card_data['customer_name'],
            phone=card_data['phone_number'],
            email=card_data['customer_email']
        )


        vehicle = self.vehicle_dao.get_or_create(
            plate_number=card_data['plate_number'],
            vehicle_type=card_data['vehicle_type']
        )


        self.monthly_card_dao.create(
            card_code=card_data['card_code'],
            customer_id=customer.id,
            vehicle_id=vehicle.id,
            monthly_fee=card_data['monthly_fee'],
            start_date=card_data['start_date'],
            expiry_date=card_data['expiry_date'],
            is_paid=card_data['is_paid']
        )


        return {
            'customer': customer,
            'vehicle': vehicle,
            'card_code': card_data['card_code']
        }
