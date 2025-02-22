import psycopg2
from fastapi import FastAPI, Request, HTTPException

try:
    conn = psycopg2.connect(
        dbname = "postgres",
        user= 'postgres',
        password = '12345678',
        host='localhost',
        port='5432'
        )
except Exception as e:
    print(f"Error connecting to the database: {e}")
    raise HTTPException(status_code=500, detail="Database connection error")

conn.set_client_encoding('UTF8')
cursor = conn.cursor()

def store_message(user_id, name, phone, order, amount):

    try:
        
        query = f"INSERT INTO data (userid, name, phone, \"order\", amount, date, time) VALUES ('{user_id}', '{name}', '{phone}', '{order}', '{amount}', CURRENT_DATE, CURRENT_TIME)"
        print(query)
        cursor.execute(query)
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database operation error")


def get_chat_history():
    return