from desktop_app.db.database import Database
from desktop_app.model.Payment import Payment


class PaymentDAO:

    def __init__(self):
        self._dbConn = Database()



    def get_all_payments(self):  

        conn = self._dbConn.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT id, card_id, monthly_card_id, amount, method, payment_date FROM payments')
        rows = cursor.fetchall()


        return [Payment(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows] 
