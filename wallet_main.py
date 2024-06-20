import tkinter.messagebox
from tkinter import *
import connection_to_db
from psycopg2 import errors
import work_with_db


def main():
    global wind1
    wind1 = Tk()
    wind1.title('V_wallet')
    wind1.geometry('360x230+825+150')
    wind1.resizable(width=True, height=True)
    wind1.config(bg='gray27')

    def login():
        global name
        name = log_name.get()
        pas = log_pass.get()
        if name and pas:
            try:
                with connection_to_db.conn.cursor() as cur:
                    data = work_with_db.login(cur, name, pas)
                if data == True:
                    balance_wind()
                    wind1.destroy()
                else:
                    tkinter.messagebox.showerror("Помилка", "Неправильно введено пароль")
            except (errors.InvalidTextRepresentation, ValueError, errors.InFailedSqlTransaction,
                    errors.StringDataRightTruncation) as e:
                tkinter.messagebox.showerror("Помилка", f"Виникла помилка: {e}")
            except TypeError:
                tkinter.messagebox.showerror("Помилка", "Такого користувача не інує")
            finally:
                cur.close()
        else:
            tkinter.messagebox.showerror("Помилка", f"Введіть всі дані")

    Label(wind1, text='Для початку роботи увійдіть в свій акаунт \n або зареєструйтесь:', font=('Roboto', 12),
          bg='gray27', fg='#117A3D').place(
        x=30, y=20)
    Label(wind1, text="Ім'я користувача:", bg='gray27', fg='#117A3D').place(x=15, y=70)
    Label(wind1, text='Пароль:', bg='gray27', fg='#117A3D').place(x=66, y=110)
    log_name = Entry(wind1, bg='gray22', fg='#117A3D')
    log_name.place(x=120, y=70)
    log_pass = Entry(wind1, bg='gray22', fg='#117A3D')
    log_pass.place(x=120, y=110)
    Button(wind1, text='Увійти', command=login, width=15, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').place(x=125, y=140)
    Button(wind1, text='Зареєструватись', command=reg_wind, width=15, bg='gray22', fg='#117A3D',
           activebackground='#117A3D', activeforeground='gray22').place(x=125, y=190)
    wind1.mainloop()


def reg_wind():
    global wind1
    wind1.destroy()
    wind2 = Tk()
    wind2.title('Вікно реєстрації')
    wind2.geometry('300x200+825+150')
    wind2.resizable(width=True, height=True)
    wind2.config(bg='gray27')

    def back():
        wind2.destroy()
        main()

    def reg():
        global name
        name = reg_name.get()
        pas = reg_pass.get()
        if name and pas:
            try:
                with connection_to_db.conn.cursor() as cur:
                    data = work_with_db.registration(cur, name, pas)
                if data == True:
                    balance_wind()
                    wind2.destroy()
            except (errors.InvalidTextRepresentation, ValueError, errors.InFailedSqlTransaction,
                    errors.StringDataRightTruncation) as e:
                tkinter.messagebox.showerror("Помилка", f"Виникла помилка: {e}")
        else:
            tkinter.messagebox.showerror("Помилка", f"Введіть всі дані")

    Label(wind2, text='Реєстрація', font=("Roboto", 20), bg='gray27', fg='#117A3D').pack()
    Label(wind2, text="Ім'я користувача:", bg='gray27', fg='#117A3D').place(x=15, y=70)
    Label(wind2, text='Пароль:', bg='gray27', fg='#117A3D').place(x=66, y=110)
    reg_name = Entry(wind2, bg='gray22', fg='#117A3D')
    reg_name.place(x=120, y=70)
    reg_pass = Entry(wind2, bg='gray22', fg='#117A3D')
    reg_pass.place(x=120, y=110)
    Button(wind2, text='Зареєструватись', command=reg, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').place(x=95, y=140)
    Button(wind2, text='Назад', command=back, width=30, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').pack(side=BOTTOM)

    wind2.mainloop()


def balance_wind():
    global name, balance, wind3
    wind3 = Tk()
    wind3.title('Гаманець')
    wind3.geometry('300x300+825+150')
    wind3.resizable(width=True, height=True)
    wind3.config(bg='gray27')

    with connection_to_db.conn.cursor() as cur:
        balance = work_with_db.balance(cur, name)

    Label(wind3, text='Ваш баланс:', font=("Roboto", 15), bg='gray27', fg='#117A3D').pack()
    Label(wind3, text=f"{balance} грн", font=("Roboto", 20), bg='gray27', fg='#117A3D').pack()

    Label(wind3, text="Операції", font=("Roboto", 12), bg='gray27', fg='#117A3D').place(x=110, y=90)
    Button(wind3, text='Зняти кошти', command=minus_window, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').place(x=105, y=120)
    Button(wind3, text='Внести кошти', command=plus_window, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').place(x=102, y=160)
    Button(wind3, text='Історія операцій', command=history_window, bg='gray22', fg='#117A3D',
           activebackground='#117A3D', activeforeground='gray22').place(x=95, y=200)


def minus_window():
    global name, balance, wind3
    wind3.destroy()
    wind4 = Tk()
    wind4.title('Гаманець')
    wind4.geometry('300x150+825+150')
    wind4.resizable(width=True, height=True)
    wind4.config(bg='gray27')

    def back():
        wind4.destroy()
        balance_wind()

    def minus():
        sum = suma.get()
        if sum:
            if int(balance) - int(sum) < 0:
                tkinter.messagebox.showerror("Помилка", f"В вас нема такої суми")
            else:
                new_balance = int(balance) - int(sum)
                with connection_to_db.conn.cursor() as cur:
                    data = work_with_db.minus(cur, name, sum, new_balance)
                    if data == True:
                        wind4.destroy()
                        balance_wind()
        else:
            tkinter.messagebox.showerror("Помилка", f"Введіть дані")

    Label(wind4, text='Введіть суму, яку хочете зняти', font=("Roboto", 12), bg='gray27', fg='#117A3D').pack()
    suma = Entry(wind4, bg='gray22', fg='#117A3D')
    suma.place(x=90, y=40)
    Button(wind4, text='Зняти кошти', command=minus, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').place(x=105, y=70)
    Button(wind4, text='Назад', command=back, width=30, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').pack(side=BOTTOM)


def plus_window():
    global name, balance, wind3
    wind3.destroy()
    wind5 = Tk()
    wind5.title('Гаманець')
    wind5.geometry('300x150+825+150')
    wind5.resizable(width=True, height=True)
    wind5.config(bg='gray27')

    def back():
        wind5.destroy()
        balance_wind()

    def plus():
        sum = suma.get()
        if sum:
            new_balance = int(balance) + int(sum)

            with connection_to_db.conn.cursor() as cur:
                data = work_with_db.plus(cur, name, sum, new_balance)
                if data == True:
                    wind5.destroy()
                    balance_wind()
        else:
            tkinter.messagebox.showerror("Помилка", f"Введіть дані")

    Label(wind5, text='Введіть суму, яку хочете внести', font=("Roboto", 12), bg='gray27', fg='#117A3D').pack()
    suma = Entry(wind5, bg='gray22', fg='#117A3D')
    suma.place(x=90, y=40)
    Button(wind5, text='Внести кошти', command=plus, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').place(x=105, y=70)
    Button(wind5, text='Назад', command=back, width=30, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').pack(side=BOTTOM)


def history_window():
    global name, wind3
    wind3.destroy()
    wind6 = Tk()
    wind6.title('Гаманець')
    wind6.geometry('300x300+825+150')
    wind6.resizable(width=True, height=True)
    wind6.config(bg='gray27')

    def back():
        wind6.destroy()
        balance_wind()

    with connection_to_db.conn.cursor() as cur:
        history = work_with_db.history(cur, name)

    if history == None:
        history_op = ["Ви ще не робили транзакцій"]
        history_op_var = Variable(value=history_op)
    else:
        history_op = str(history).split(', ')
        history_op_var = Variable(value=history_op)

    Label(wind6, text='Історія транзакцій:', font=("Roboto", 12), bg='gray27', fg='#117A3D').pack()
    Button(wind6, text='Назад', command=back, width=30, bg='gray22', fg='#117A3D', activebackground='#117A3D',
           activeforeground='gray22').pack(side=BOTTOM)
    history_listbox = Listbox(listvariable=history_op_var, bg='gray22', fg='#117A3D')
    history_listbox.pack(side=LEFT, fill=BOTH, expand=1)
    history_scrollbar = Scrollbar(orient="vertical", command=history_listbox.yview)
    history_scrollbar.pack(side=RIGHT, fill=Y)
    history_listbox["yscrollcommand"] = history_scrollbar.set


if __name__ == '__main__':
    main()
