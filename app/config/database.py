import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Database:
    def __init__(self) -> None:
        self.conn = self.connect()

    def connect(self):

        cursor = None
        conn = None

        while True:
            try:
                conn = psycopg2.connect(host='localhost', database='investments', user='postgres', password='password',
                cursor_factory=RealDictCursor)
                cursor = conn.cursor()
                print("Database connection was succesfull!")
                break
            except Exception as error:
                print("Connecting to Dabase failed")
                print(f"The error was: {error}")
                time.sleep(2)

        return conn, cursor