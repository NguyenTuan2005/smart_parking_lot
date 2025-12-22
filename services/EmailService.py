import smtplib
from email.mime.text import MIMEText
from config.email_config import *

class EmailService:

    def __init__(self):
        self.server = SMTP_SERVER
        self.port = SMTP_PORT
        self.username = EMAIL_USERNAME
        self.password = EMAIL_PASSWORD

    def send_email(self, to_email, subject, content):
        msg = MIMEText(content, "plain", "utf-8")
        msg["From"] = f"{DEFAULT_FROM_NAME} <{self.username}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        self._send(msg)


    def _send(self, msg):
        with smtplib.SMTP(self.server, self.port) as smtp:
            smtp.starttls()
            smtp.login(self.username, self.password)
            smtp.send_message(msg)


