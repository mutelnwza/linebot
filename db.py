import psycopg2

conn = psycopg2.connect(
    dbname = "linebot_database_4mwg",
    user= 'linebot_database_4mwg_user',
    password = 'uSVf4L5FZOA3SEkRj69csPuyDUhULMnS',
    host='dpg-curc23rqf0us73fhs56g-a.singapore-postgres.render.com',
    port='5432'
    )

cursor = conn.cursor()

def store_message(sender, user_id, user_name, message):

    query = "INSERT INTO {sender} (user_id, name, time, text) VALUES ({id}, {name}, NOW();, {text})".format(sender = sender, id = user_id, name = user_name, text = message)
    print(query)
    cursor.execute(query)
    conn.commit()
