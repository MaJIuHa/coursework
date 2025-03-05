from PyQt5 import QtWidgets, QtGui
from db.core import PGSession
from db.models import  Users
from sqlalchemy import select
from ui.panel import SuperAdminPanel, AdminPanel, UserPanel

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аутентификация")
        self.setGeometry(100, 100, 500, 400)
        self.setFixedSize(500, 400)

        layout = QtWidgets.QVBoxLayout()

        label_username = QtWidgets.QLabel("Логин:")
        label_username.setFont(QtGui.QFont("Arial", 15))
        layout.addWidget(label_username)

        self.entry_username = QtWidgets.QLineEdit()
        self.entry_username.setFont(QtGui.QFont("Arial", 13))
        layout.addWidget(self.entry_username)

        label_password = QtWidgets.QLabel("Пароль:")
        label_password.setFont(QtGui.QFont("Arial", 15))
        layout.addWidget(label_password)

        self.entry_password = QtWidgets.QLineEdit()
        self.entry_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.entry_password.setFont(QtGui.QFont("Arial", 13))
        layout.addWidget(self.entry_password)

        btn_login = QtWidgets.QPushButton("Войти")
        btn_login.setFont(QtGui.QFont("Arial", 13))
        btn_login.clicked.connect(self.login)
        layout.addWidget(btn_login)

        self.setLayout(layout)

    def login(self):
        username = self.entry_username.text()
        password = self.entry_password.text()

        with PGSession() as session:
            stmt = select(Users).where((Users.login == username) and (Users.password == password))
            user = session.execute(stmt).scalars().first()

            if user:
                QtWidgets.QMessageBox.information(self, "Успех", f"Вход выполнен! Ваша роль: {user.role}")
                
                if user.role == "superadmin":
                    self.panel = SuperAdminPanel()
                elif user.role == "admin":
                    self.panel = AdminPanel()
                elif user.role == "user":
                    self.panel = UserPanel()
                
                self.panel.show()
            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")