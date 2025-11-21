from typing import Set
from desktop_app.db.database import Database
from desktop_app.model.Customer import Customer

class CustomerDAO:
    def __init__(self):
        self._db = Database()

    def get_all(self):
        conn = self._db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, full_name, phone_number, email FROM Customers")
        rows = cursor.fetchall()
   
        customers = [Customer(row[0], row[1], row[2], row[3]) for row in rows]
        return customers


    def get_by_id(self, customer_id: int):
        conn = self._db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM Customers WHERE id = ?", (customer_id,))
        row = cursor.fetchone()
        if row:
            return Customer(row[0], row[1], row[2], row[3])
        return None


    def update(self, customer):
       conn = self._db.connect()
       cursor = conn.cursor()
       cursor.execute(
           "UPDATE Customers SET fullname = ?, phone_number = ?, email = ? WHERE id = ?",
           (customer.name, customer.phone_number, customer.email, customer.id)
       )

       cursor.commit()
       

    def add_customer(self, customer):
        conn = self._db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Customers (fullname, phone_number, email) VALUES (?, ?)",
            (customer.name, customer.phone_number , customer.email)
        )
        conn.commit()
       

    def delete_customer(self, customer_id):
        conn = self._db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customers WHERE id = ?", (customer_id,))
        conn.commit()     