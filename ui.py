import tkinter as tk
from tkinter import messagebox

# Функция обработки входа
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    # Пример проверки (замените на проверку с базой данных)
    if username == "admin" and password == "1234":
        messagebox.showinfo("Успех", "Добро пожаловать!")
        root.destroy()  # Закрываем окно после успешного входа
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

# Создание окна
root = tk.Tk()
root.title("Аутентификация")
root.geometry("500x400")
root.resizable(False, False)

# Основной фрейм для центрирования
frame = tk.Frame(root)
frame.pack(expand=True)

# Метка и поле для логина
tk.Label(frame, text="Логин:", font=("Arial", 15)).pack(pady=10)
entry_username = tk.Entry(frame, font=("Arial", 13), width=15)
entry_username.pack(pady=10)

# Метка и поле для пароля
tk.Label(frame, text="Пароль:", font=("Arial", 15)).pack(pady=10)
entry_password = tk.Entry(frame, show="*", font=("Arial", 13), width=15)
entry_password.pack(pady=10)

# Кнопка входа
btn_login = tk.Button(frame, text="Войти", font=("Arial", 13), width=11, height=1, command=login)
btn_login.pack(pady=30)

# Запуск цикла обработки событий
root.mainloop()




# Фейковая база пользователей
users_db = {
    "superadmin": {"password": "root123", "role": "superadmin"},
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
}

# Функция обработки входа
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username in users_db and users_db[username]["password"] == password:
        role = users_db[username]["role"]
        messagebox.showinfo("Успех", f"Вход выполнен! Ваша роль: {role}")
        root.destroy()
        open_dashboard(role)
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

# Функция панели управления
def open_dashboard(role):
    dashboard = tk.Tk()
    dashboard.title("Панель управления")
    dashboard.geometry("500x400")
    
    frame = tk.Frame(dashboard)
    frame.pack(expand=True)

    tk.Label(frame, text=f"Добро пожаловать, {role}!", font=("Arial", 15)).pack(pady=10)

    if role == "superadmin":
        tk.Label(frame, text="Полный доступ", font=("Arial", 13)).pack(pady=10)
        tk.Button(frame, text="Редактировать пользователей", font=("Arial", 12), width=22).pack(pady=5)
        tk.Button(frame, text="Настройки системы", font=("Arial", 12), width=22).pack(pady=5)
    
    elif role == "admin":
        tk.Label(frame, text="Просмотр всех данных + редактирование", font=("Arial", 13)).pack(pady=10)
        tk.Button(frame, text="Просмотр пользователей", font=("Arial", 12), width=22).pack(pady=5)
        tk.Button(frame, text="Редактировать номера", font=("Arial", 12), width=22).pack(pady=5)
    
    elif role == "user":
        tk.Label(frame, text="Только просмотр данных", font=("Arial", 13)).pack(pady=10)
        tk.Button(frame, text="Просмотр доступных номеров", font=("Arial", 12), width=22).pack(pady=5)

    dashboard.mainloop()

# Создание окна авторизации
root = tk.Tk()
root.title("Аутентификация")
root.geometry("500x400")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(expand=True)

tk.Label(frame, text="Логин:", font=("Arial", 15)).pack(pady=10)
entry_username = tk.Entry(frame, font=("Arial", 13), width=15)
entry_username.pack(pady=10)

tk.Label(frame, text="Пароль:", font=("Arial", 15)).pack(pady=10)
entry_password = tk.Entry(frame, show="*", font=("Arial", 13), width=15)
entry_password.pack(pady=10)

btn_login = tk.Button(frame, text="Войти", font=("Arial", 13), width=11, height=1, command=login)
btn_login.pack(pady=30)

root.mainloop()
