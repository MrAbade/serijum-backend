from psycopg2 import connect
from csv import DictReader
from os import getenv

DATABASE = getenv('DATABASE')
USER = getenv('USER')
PASSWORD = getenv('PASSWORD')
HOST = getenv('HOST')

FILENAME = 'database_injection/suites.csv'


def open_suites(filename):
    with open(filename, 'r') as file:
        for suite in DictReader(file):
            yield suite


def insert_into_database(filename, conn, cursor):
    for suite in open_suites(filename):
        category_id = suite['category_id']
        suite_number = suite['suite_number']
        suite_name = suite['suite_name']

        cursor.execute("""
        INSERT INTO suites (category_id, suite_number, suite_name)
        VALUES(%s, %s, %s);
        """, (category_id, suite_number, suite_name,))

    conn.commit()


conn = connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)
cursor = conn.cursor()

insert_into_database(FILENAME, conn, cursor)
