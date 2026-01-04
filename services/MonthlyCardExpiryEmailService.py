import os
import smtplib
from email.mime.text import MIMEText
from config.email_config import *
from dao.CustomerDAO import CustomerDAO


class MonthlyCardExpiryEmailService:

    def __init__(self):
        self.customer_dao = CustomerDAO()
        self.email_service = EmailService()

    def notify_customers_expiring_card(self, days=3):
        customers = self.customer_dao.get_users_expiring_in_days(days)

        template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "card_expiry.html")
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                template = f.read()
        except FileNotFoundError:
            print(f"Warning: Template file {template_path} not found. Using plain text fallback.")
            template = None

        for c in customers:
            name = c.fullname
            email = c.email
            expiry_date = c.expiry_date.strftime("%d/%m/%Y")

            if template:
                html_content = template.replace("{{name}}", name).replace("{{expiry}}", expiry_date)
                self.email_service.send_html_email(
                    to_email=email,
                    subject="Thông báo thẻ sắp hết hạn",
                    html_content=html_content
                )
            else:
                content = (
                    f"Xin chào {name},\n\n"
                    f"Thẻ của bạn sẽ hết hạn vào ngày {expiry_date}.\n"
                    f"Vui lòng gia hạn sớm để tránh gián đoạn sử dụng dịch vụ.\n\n"
                    f"— Hệ thống quản lý bãi xe—"
                )
                self.email_service.send_plain_email(
                    to_email=email,
                    subject="Thông báo thẻ sắp hết hạn",
                    content=content
                )

            self.customer_dao.mark_notified(c.customer_id) #đánh dấu đã thông báo


class EmailService:

    def __init__(self):
        self.server = SMTP_SERVER
        self.port = SMTP_PORT
        self.username = EMAIL_USERNAME
        self.password = EMAIL_PASSWORD

    def send_plain_email(self, to_email, subject, content):
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = f"{DEFAULT_FROM_NAME} <{self.username}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        self._send(msg)

    def send_html_email(self, to_email, subject, html_content):
        msg = MIMEText(html_content, "html", "utf-8")
        msg["From"] = f"{DEFAULT_FROM_NAME} <{self.username}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        self._send(msg)


    def _send(self, msg):
        with smtplib.SMTP(self.server, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.send_message(msg)