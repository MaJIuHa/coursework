import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Подключение к PostgreSQL
DATABASE_URL = "postgresql://postgres:1234@localhost/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Модель таблицы пользователей
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

# Функция проверки аутентификации
def login():
    username = entry_username.get()
    password = entry_password.get()

    user = session.query(User).filter_by(login=username, password=password).first()

    if user:
        messagebox.showinfo("Успех", f"Вход выполнен! Ваша роль: {user.role}")
        root.destroy()
        open_dashboard(user.role)
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

# Панель управления
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

# Окно авторизации
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