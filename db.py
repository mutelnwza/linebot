import psycopg2
from fastapi import FastAPI, Request, HTTPException

try:
    conn = psycopg2.connect(
        dbname = "linebot_database_4mwg",
        user= 'linebot_database_4mwg_user',
        password = 'uSVf4L5FZOA3SEkRj69csPuyDUhULMnS',
        host='dpg-curc23rqf0us73fhs56g-a.singapore-postgres.render.com',
        port='5432'
        )
except Exception as e:
    print(f"Error connecting to the database: {e}")
    raise HTTPException(status_code=500, detail="Database connection error")

cursor = conn.cursor()

def store_message(sender, user_id, user_name, message):

    try:
        query = "INSERT INTO user_db (userid, name, time, text, sender) VALUES ('{id}', '{name}', NOW(), '{text}', '{sender}');".format(sender = sender, id = user_id, name = user_name, text = message)
        print(query)
        cursor.execute(query)
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database operation error")
    

def store_user_data(user_id, user_name):
    try:
        query = "INSERT INTO user_info (userid, name, time_added) VALUES ('{id}', '{name}', NOW()) ON CONFLICT (userid) DO NOTHING;".format(id=user_id, name=user_name)
        print(query)
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database operation error")
    

def get_chat_history():
    return