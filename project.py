import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview

# Создание базы данных и таблицы
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS employees 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  full_name TEXT, 
                  phone_number TEXT, 
                  email TEXT, 
                  salary TEXT)''')
conn.commit()
employees_data = [
    (1, 'Pasha', '+89451423245', 'pasha@gmail.com', '100к'),
    (2, 'Антон', '+81200400645', 'anton@mail.ru', '110к'),
    (3, 'Алекскей', '+89184561278', 'alex@gmail.ru', '260к'),
    (4, 'Андрей', '+84516481528', 'andrey@yandex.ru', '60к'),
    (5, 'Сергей', '+78494982824', 'sergey@gmail.com', '100к'),
]
cursor.executemany('INSERT OR IGNORE INTO employees (id, full_name, phone_number, email, salary) VALUES (?, ?, ?, ?, ?)', employees_data)
# Функция для добавления нового сотрудника
def add_employee():
    full_name = entry_full_name.get()
    phone_number = entry_phone_number.get()
    email = entry_email.get()
    salary = entry_salary.get()

    if full_name and phone_number and email and salary:
        cursor.execute("INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)",
                       (full_name, phone_number, email, salary))
        conn.commit()
        messagebox.showinfo("Успешно!", "Сотрдуник добавлен.")
    else:
        messagebox.showerror("Ошибка!", "Проверьте, пожалуйста, ввод.")

# Функция для изменения информации о сотруднике
def update_employee():
    selected_item = treeview.focus()
    if selected_item:
        employee_id = treeview.item(selected_item)['values'][0]
        full_name = entry_full_name.get()
        phone_number = entry_phone_number.get()
        email = entry_email.get()
        salary = entry_salary.get()

        if full_name and phone_number and email and salary:
            cursor.execute("UPDATE employees SET full_name=?, phone_number=?, email=?, salary=? WHERE id=?",
                           (full_name, phone_number, email, salary, employee_id))
            conn.commit()
            messagebox.showinfo("Успешно!", "Данные о сотрдунике обновлены.")
        else:
            messagebox.showerror("Ошибка!", "Проверьте, пожалуйста, ввод.")
    else:
        messagebox.showerror("Error", "Please select an employee")

# Функция для удаления сотрудника
def delete_employee():
    selected_item = treeview.focus()
    if selected_item:
        result = messagebox.askyesno("Уверенны, что хотите удалить?")
        if result:
            employee_id = treeview.item(selected_item)['values'][0]
            cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
            conn.commit()
            messagebox.showinfo("Успешно!", "Сотрудник удалён.")
    else:
        messagebox.showerror("Ошибка!", "Проверьте, пожалуйста, ввод.")


# Создание графического интерфейса
root = Tk()
root.title("Employee List")

# Создание виджетов
label_full_name = Label(root, text="Full Name")
label_full_name.grid(row=0, column=0)
entry_full_name = Entry(root)
entry_full_name.grid(row=0, column=1)

label_phone_number = Label(root, text="Phone Number")
label_phone_number.grid(row=1, column=0)
entry_phone_number = Entry(root)
entry_phone_number.grid(row=1, column=1)

label_email = Label(root, text="Email")
label_email.grid(row=2, column=0)
entry_email = Entry(root)
entry_email.grid(row=2, column=1)

label_salary = Label(root, text="Salary")
label_salary.grid(row=3, column=0)
entry_salary = Entry(root)
entry_salary.grid(row=3, column=1)

button_add = Button(root, text="Add Employee", command=add_employee)
button_add.grid(row=4, column=0)

button_update = Button(root, text="Update Employee", command=update_employee)
button_update.grid(row=4, column=1)

button_delete = Button(root, text="Delete Employee", command=delete_employee)
button_delete.grid(row=4, column=2)



treeview = Treeview(root, columns=("ID", "Full Name", "Phone Number", "Email", "Salary"))
treeview.heading("ID", text="ID")
treeview.heading("Full Name", text="Full Name")
treeview.heading("Phone Number", text="Phone Number")
treeview.heading("Email", text="Email")
treeview.heading("Salary", text="Salary")
treeview.column("#0", width=0, stretch=NO)
treeview.column("ID", width=30, anchor=CENTER)
treeview.column("Full Name", width=150, anchor=W)
treeview.column("Phone Number", width=100, anchor=W)
treeview.column("Email", width=150, anchor=W)
treeview.column("Salary", width=80, anchor=E)
treeview.grid(row=6, column=0, columnspan=3)

root.mainloop()

# Закрытие соединения с базой данных
conn.close()