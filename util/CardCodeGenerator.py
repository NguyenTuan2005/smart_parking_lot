class CardCodeGenerator:
    @staticmethod
    def generate_next_single_card_code(last_code: str) -> str:
        if not last_code:
            return "C0001"

        try:
            prefix = "C"
            number_part = last_code[len(prefix) :]
            next_number = int(number_part) + 1
            return f"{prefix}{next_number:04d}"
        except (ValueError, TypeError):
            return "C0001"

    @staticmethod
    def generate_next_monthly_card_code(last_code: str) -> str:
        if not last_code:
            return "MC0001"

        try:
            prefix = "MC"
            number_part = last_code[len(prefix) :]
            next_number = int(number_part) + 1
            return f"{prefix}{next_number:04d}"
        except (ValueError, TypeError):
            return "MC0001"
