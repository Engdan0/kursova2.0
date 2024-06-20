from tkinter import *
import tkinter
from psycopg2 import errors
from datetime import datetime


def registration(cur, name, pas):
    try:
        cur.execute(f'''SELECT name FROM "users" ''')
        get_data = cur.fetchall()
        for i in get_data:
            if str(name) == str(i[0]):
                tkinter.messagebox.showerror("Помилка", f"Такий користувач вже існує")
                return False

        cur.execute('SELECT MAX(id) FROM "users" ')
        next_id = cur.fetchall()
        insert_data_to_db = (f'''INSERT INTO "users"(
                                        id, name, password, balance)
                                       VALUES (%s, %s, %s, %s)''')
        data = (next_id[-1][0] + 1, name, pas, 0)
        cur.execute(insert_data_to_db, data)
        cur.connection.commit()
        return True
    except (errors.InvalidTextRepresentation, ValueError, errors.InFailedSqlTransaction,
            errors.StringDataRightTruncation) as e:
        raise e
    finally:
        cur.close()


def login(cur, name, pas):
    try:
        cur.execute(f'''SELECT password, name FROM "users" Where name = %s''', (name,))
        get_data = cur.fetchone()
        if get_data[0] == pas:
            return True
        else:
            return False
    except (errors.InvalidTextRepresentation, ValueError, errors.InFailedSqlTransaction,
            errors.StringDataRightTruncation) as e:
        raise e
    except TypeError:
        raise
    finally:
        cur.close()


def balance(cur,name):
    cur.execute(f'''SELECT balance FROM "users" Where name = %s''', (name,))
    balance = cur.fetchone()[0]
    return balance


def minus(cur,name,sum,new_balance):
    cur.execute(f'''SELECT history FROM "users" Where name = %s''', (name,))
    history = cur.fetchone()[0]
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y,%H:%M:%S")
    if history != None:
        operation = history + f" -{sum} ({dt_string}),"
    else:
        operation = f" -{sum} ({dt_string}),"

    cur.execute(f'''UPDATE "users" SET balance = %s, history = %s WHERE name = %s''',
                (new_balance, operation, name,))
    cur.connection.commit()
    return True

def plus(cur,name,sum,new_balance):
    cur.execute(f'''SELECT history FROM "users" Where name = %s''', (name,))
    history = cur.fetchone()[0]
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y,%H:%M:%S")
    if history != None:
        operation = history + f" -{sum} ({dt_string}),"
    else:
        operation = f" -{sum} ({dt_string}),"

    cur.execute(f'''UPDATE "users" SET balance = %s, history = %s WHERE name = %s''',
               (new_balance, operation, name,))
    cur.connection.commit()
    return True

def history(cur,name):
    cur.execute(f'''SELECT history FROM "users" Where name = %s''', (name,))
    history = cur.fetchone()[0]
    return history
