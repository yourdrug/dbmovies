import psycopg2
from dotenv import dotenv_values

config = dotenv_values(".env")


class MovieDb:
    def __init__(self):
        self.conn = psycopg2.connect(database=config["POSTGRES_DB"], user=config["POSTGRES_USER"], host=config["HOST"],
                                     port=config["PORT"], password=config["POSTGRES_PASSWORD"])

    def get_cursor(self):
        return self.conn.cursor()
