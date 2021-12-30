import psycopg2 as pg
import logging
from os import environ as env
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")

def database_connect():
    # TODO return an open connection
    try:
        db_connection = pg.connect(host=env["PG_HOST"],
                                   database="postgres",
                                   user=env["PG_USER"],
                                   password=env["PG_P"],
                                   port=env["PG_PORT"])
        print('connect to db postgres')
        db_connection.autocommit = True
        cur = db_connection.cursor()
        try:
            cur.execute(f"""CREATE DATABASE {env["PG_DB"]}""")
            db_connection = pg.connect(host=env["PG_HOST"],
                                        database=env["PG_DB"],
                                        user=env["PG_USER"],
                                        password=env["PG_P"],
                                        port=env["PG_PORT"])
            print(f"""connect to db {env["PG_DB"]}""")
            db_connection.autocommit = True
            cur = db_connection.cursor()
        except Exception as err:
            logging.error(err)
            db_connection = pg.connect(host=env["PG_HOST"],
                                        database=env["PG_DB"],
                                        user=env["PG_USER"],
                                        password=env["PG_P"],
                                        port=env["PG_PORT"])
            print(f"""connect to db {env["PG_DB"]}""")
            db_connection.autocommit = True
            cur = db_connection.cursor()
        return db_connection,cur
    except pg.DatabaseError as err:
        logging.error(err)

def db_operation(cursor,command,inputs):
    if command == "create":
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {env["PG_TABLE"]}({inputs})""")
    elif command == "insert":
        for data in inputs:
            cursor.execute(f"""INSERT INTO {env["PG_TABLE"]} (brand,oil_type,oil_price,scraping_date) VALUES {data}""")

