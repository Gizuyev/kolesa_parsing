import csv
import psycopg2

DB_NAME = "kolesa_db"
DB_USER = "admin"
DB_PASSWORD = "12345"
DB_HOST = "localhost"

csv_file_path = "/home/ibragim/python_mor/parsing/kolesa/cars.csv"

def insert_data_from_csv():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST,
    )
    cur = conn.cursor()

    with open(csv_file_path, "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)

        for row in csvreader:
            marka, title, year, type_car, ob, type_topliva, kpp, price, city, date, views, picture, link = row

            insert_query = """
            INSERT INTO cars (marka, title, year, type_car, ob, type_topliva, kpp, price, city, date, views, picture, link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            cur.execute(
                insert_query,
                (marka, title, year, type_car, ob, type_topliva, kpp, price, city, date, views, picture, link),
            )

    conn.commit()
    conn.close()

insert_data_from_csv()

