import re


class Validator:
    @staticmethod
    def is_valid_email(email: str) -> bool:
        if not email:
            return False
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        if not phone:
            return False
        phone_regex = r"^0[0-9]{9}$"
        return re.match(phone_regex, phone) is not None
