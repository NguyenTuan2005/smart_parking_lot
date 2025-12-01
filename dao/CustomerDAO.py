from typing import List, Optional
from db.database import Database
from model.Customer import Customer


class CustomerDAO:
    def __init__(self):
        self.__db = Database()

    def get_all_customers(self) -> List[Customer]:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute("SELECT id, full_name, phone_number, email FROM customers")
        rows = cursor.fetchall()

        customers = [
            Customer(row[0], row[1], row[2], row[3])
            for row in rows
        ]

        cursor.close()
        conn.close()

        return customers

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, full_name, phone_number, email FROM customers WHERE id = ?",
            (customer_id,)
        )

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Customer(row[0], row[1], row[2], row[3])
        return None

    def update(self, customer: Customer) -> None:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE customers 
            SET full_name = ?, phone_number = ?, email = ?
            WHERE id = ?
            """,
            (customer.fullname, customer.phone_number, customer.email, customer.id)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def add_customer(self, customer: Customer) -> None:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO customers (full_name, phone_number, email)
            VALUES (?, ?, ?)
            """,
            (customer.fullname, customer.phone_number, customer.email)
        )

        conn.commit()
        cursor.close()
        conn.close()

    def delete_customer(self, customer_id: int) -> None:
        conn = self.__db.connect()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM customers WHERE id = ?",
            (customer_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    customer_dao = CustomerDAO()
    print(customer_dao.get_all_customers())