import psycopg2

conn = psycopg2.connect(dbname="wallet", user="postgres", password="1234", host="localhost", port="5432")
cursor = conn.cursor()

# создаем таблицу people
cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(50),  password VARCHAR(50), balance INTEGER, history VARCHAR)")
# поддверждаем транзакцию
conn.commit()
print("Таблица people успешно создана")

cursor.close()
conn.close()