import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

load_dotenv()

DATABASE = os.getenv("DATABASE")
USER_DB = os.getenv("USER_DB")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

# Create connection object conn
conn = psycopg2.connect(
    database=DATABASE, user=USER_DB, password=PASSWORD, host=HOST, port=PORT
)

# cursor allows Python code to execute PostgreSQL commands in a database session
cur = conn.cursor()
cur.execute("SELECT * FROM eda.king_county_house_sales LIMIT 10")
rows = cur.fetchall()
for row in rows:
    print(row)


# import the data into a pandas dataframe
query_string = """
     SELECT d.*, s.id AS sale_id, s.date, s.price
    FROM eda.king_county_house_details AS d
    LEFT JOIN eda.king_county_house_sales AS s
    ON d.id = s.house_id
"""
df_psycopg = pd.read_sql(query_string, conn)

count = pd.read_sql("SELECT COUNT(*) FROM eda.king_county_house_details", conn).iloc[0, 0]
print(count)


# close the connection
conn.close()

df_psycopg.head()

# export the data to a csv-file
df_psycopg.to_csv("data/eda.csv", index=False)
print(df_psycopg.shape)