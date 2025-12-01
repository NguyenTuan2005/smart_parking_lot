from dao.CardDAO import CardDAO
from db.database import Database
from model.Payment import Payment


class PaymentDAO:
    def __init__(self):
        self.__db = Database()

    def get_all(self):
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM payments')
        rows = cursor.fetchall()

        return {Payment(row.id,
                        CardDAO().get_by_id(
                            row.card_id) if row.card_id is not None else CardDAO().get_monthly_card_by_id(
                            row.monthly_card_id),
                        row.amount,
                        row.method,
                        row.payment_date) for row in rows}