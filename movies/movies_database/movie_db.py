import psycopg2
from psycopg2 import pool
from dotenv import dotenv_values
from contextlib import contextmanager

config = dotenv_values(".env")


class MovieDb:
    def __init__(self):
        db_config = {
            'database': config["POSTGRES_DB"],
            'user': config["POSTGRES_USER"],
            'host': config["HOST"],
            'port': config["PORT"],
            'password': config["POSTGRES_PASSWORD"]
        }
        self.db_pool = psycopg2.pool.SimpleConnectionPool(1, 20, **db_config)

    @contextmanager
    def connect(self):
        conn = self.db_pool.getconn()
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def execute_query(self, query: str):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            return data
