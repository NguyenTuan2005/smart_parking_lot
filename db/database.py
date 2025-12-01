import pyodbc

class Database:
    def __init__(self):
        self.server = 'localhost'
        self.database = 'SmartParkingLotSystem'
        self.username = 'sa'
        self.password = '1111'
        self.conn = None

    def connect(self):
        return pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={self.server};DATABASE={self.database};'
            f'UID={self.username};PWD={self.password}'
        )

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
