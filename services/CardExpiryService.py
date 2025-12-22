from dao.CustomerDAO import CustomerDAO
from services.EmailService import EmailService

class CardExpiryService:

    def __init__(self, customer_dao):
        self.customer_dao = customer_dao
        self.email_service = EmailService()

    def notify_customers_expiring_card(self, days=3):
        customers = self.customer_dao.get_users_expiring_in_days(days)

        for c in customers:
            name = c.fullname
            email = c.email
            expiry_date = c.expiry_date.strftime("%d/%m/%Y")

            print(name)
            print(email)
            print(expiry_date)
            content = (
                f"Xin chào {name},\n\n"
                f"Thẻ của bạn sẽ hết hạn vào ngày {expiry_date}.\n"
                f"Vui lòng gia hạn sớm để tránh gián đoạn sử dụng dịch vụ.\n\n"
                f"— Hệ thống quản lý bãi xe—"
            )

            self.email_service.send_email(
                to_email=email,
                subject="Thông báo thẻ sắp hết hạn",
                content=content
            )


            # self.customer_dao.mark_notified(c.customer_id)


if __name__ == '__main__':
    s = CardExpiryService(CustomerDAO())
    s.notify_customers_expiring_card(9)
