import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

class Database:
#    def __init__(self) -> None:
#        self.conn = self.connect()
#
    db_host = settings.DATABASE_HOST
    db_name = settings.DATABASE_NAME
    db_user = settings.DATABASE_USER
    db_password = settings.DATABASE_PASSWORD

    def connect(self):
        cursor = None
        conn = None

        while True:
            try:
                conn = psycopg2.connect(host=self.db_host, database=self.db_name, user=self.db_user, password=self.db_password,
                cursor_factory=RealDictCursor)
                cursor = conn.cursor()

                # DEPRECATED LOGIC TO CREATE TABLE ON FIRST APP EXECUTION.
                # cursor.execute("""
                #                 CREATE TABLE IF NOT EXISTS public.users (
                #                 id serial4 NOT NULL,
                #                 "name" varchar NOT NULL,
                #                 email varchar NOT NULL,
                #                 "password" varchar NOT NULL,
                #                 created_at timestamptz NOT NULL DEFAULT now(),
                #                 CONSTRAINT users_email_key UNIQUE (email),
                #                 CONSTRAINT users_pkey PRIMARY KEY (id)
                #                 );
                #                 """)
                # conn.commit()
                # cursor.execute("""
                #                 CREATE TABLE IF NOT EXISTS public.investments (
                #                 id serial4 NOT NULL,
                #                 user_id int NOT NULL,
                #                 investment_name varchar NOT NULL,
                #                 "token" varchar NULL,
                #                 amount float4 NOT NULL,
                #                 opening_at timestamptz NOT NULL DEFAULT now(),
                #                 CONSTRAINT investments_pkey PRIMARY KEY (id),
                #                 CONSTRAINT investments_fk FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE
                #                 );
                #             """)
                # conn.commit()
                print("Database connection was succesfull!")
                break
            except Exception as error:
                print("Connecting to Database failed")
                print(f"The error was: {error}")
                time.sleep(2)
        return conn, cursor

    
    def disconnect(self):
        self.conn.close()
        print("conexion cerrada")

if __name__=='__main__':
    db = Database().connect()

