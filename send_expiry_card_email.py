
from dao.CustomerDAO import CustomerDAO
from datetime import datetime
from services.CardExpiryService import CardExpiryService

LOG_FILE = "email_sending_log.txt"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def main():
    log("START sending expiry card email")
    service = CardExpiryService(CustomerDAO())
    service.notify_customers_expiring_card(days=9)
    log("END sending expiry card email")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"ERROR: {e}")

