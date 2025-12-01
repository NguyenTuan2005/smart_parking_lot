from typing import Set

from db.database import Database
from model.Customer import Customer

class CustomerDAO:
    def __init__(self):
        self.__db = Database()

    def get_all_customers(self) -> Set[Customer]:
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()

        return {Customer(row.id, row.full_name, row.phone_number, row.email) for row in rows}

    def get_by_id(self, id: int) -> Customer or None:
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM customers WHERE id = {id}')
        customer = cursor.fetchone()
        if customer:
            return Customer(customer.id,
                            customer.full_name,
                            customer.phone_number,
                            customer.email)
        return None

        # customers = []
        # for row in cursor.fetchall():
        #     customers.append(Customer(row[0], row[1],row[2], row[3]))
        # return customers

    # def get_customer_by_id(self, customer_id):
    #     conn = self.db.connect()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT id, name, email FROM Customers WHERE id = ?", (customer_id,))
    #     row = cursor.fetchone()
    #     if row:
    #         return Customer(id=row[0], name=row[1], email=row[2])
    #     return None

    def update(self, customer):
       conn = self.__db.connect()
       cursor = conn.cursor()
       cursor.execute(
           "UPDATE Customers SET fullname = ?, phone_number = ?, email = ? WHERE id = ?",
           (customer.name, customer.phone_number, customer.email, customer.id)
       )

       cursor.commit()
       


    def add_customer(self, customer):
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Customers (fullname, phone_number, email) VALUES (?, ?)",
            (customer.name, customer.phone_number , customer.email)
        )
        conn.commit()
       


    def delete_customer(self, customer_id):
        conn = self.__db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customers WHERE id = ?", (customer_id,))
        conn.commit()