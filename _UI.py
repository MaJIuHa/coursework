from PyQt5 import QtWidgets, QtGui, QtCore
from sqlalchemy import create_engine, Column, Integer, String, func, select
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, date

from db.core import PGSession

from typing import List

from db.models import Hotel, Room, Users, Review, Client, Booking, Worker, WorkerType








    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление персоналом")
        self.setGeometry(150, 150, 1000, 600)

        layout = QtWidgets.QVBoxLayout()

        # Таблица для отображения работников
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "ID", "Отель", "Имя", "Фамилия", "Должность", 
            "Зарплата", "Email", "Адрес", "Телефон",
            "Дата начала", "Дата окончания"
        ])
        layout.addWidget(self.table)

        buttons_layout = QtWidgets.QHBoxLayout()

        # Кнопки управления
        add_employee_button = QtWidgets.QPushButton("Добавить работника")
        add_employee_button.setFont(QtGui.QFont("Arial", 12))
        add_employee_button.clicked.connect(self.add_employee)
        buttons_layout.addWidget(add_employee_button)

        delete_employee_button = QtWidgets.QPushButton("Удалить работника")
        delete_employee_button.setFont(QtGui.QFont("Arial", 12))
        delete_employee_button.clicked.connect(self.delete_employee)
        buttons_layout.addWidget(delete_employee_button)

        update_salary_button = QtWidgets.QPushButton("Изменить зарплату")
        update_salary_button.setFont(QtGui.QFont("Arial", 12))
        update_salary_button.clicked.connect(self.update_salary)
        buttons_layout.addWidget(update_salary_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        
        self.load_employees()

    def load_employees(self):
        """Загрузка списка работников в таблицу"""
        try:
            with PGSession() as session:
                # Получаем только активных работников
                query = select(Worker, Hotel.title).join(Hotel).where(Worker.is_active == True)
                workers = session.execute(query).all()
                
                self.table.setRowCount(0)  # Очищаем таблицу
                self.table.setRowCount(len(workers))
                
                for row, (worker, hotel_title) in enumerate(workers):
                    self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(worker.id)))
                    self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(hotel_title))
                    self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(worker.name))
                    self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(worker.surname))
                    self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(worker.type))
                    self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(worker.salary)))
                    self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(worker.email))
                    self.table.setItem(row, 7, QtWidgets.QTableWidgetItem(worker.address))
                    self.table.setItem(row, 8, QtWidgets.QTableWidgetItem(worker.phone))
                    self.table.setItem(row, 9, QtWidgets.QTableWidgetItem(worker.date_start.strftime('%d.%m.%Y')))
                    self.table.setItem(row, 10, QtWidgets.QTableWidgetItem('-'))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке списка работников: {str(e)}")

    def add_employee(self):
        """Добавление нового работника"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Добавление работника")
        layout = QtWidgets.QFormLayout()

        # Получаем список отелей
        with PGSession() as session:
            hotels = session.execute(select(Hotel.id, Hotel.title)).all()
            hotel_dict = {hotel[1]: hotel[0] for hotel in hotels}

        # Создаем элементы формы
        hotel_input = QtWidgets.QComboBox()
        hotel_input.addItems(hotel_dict.keys())
        name_input = QtWidgets.QLineEdit()
        surname_input = QtWidgets.QLineEdit()
        type_input = QtWidgets.QComboBox()
        type_input.addItems(["Администратор", "Менеджер", "Уборщик", "Технический специалист"])
        salary_input = QtWidgets.QSpinBox()
        salary_input.setRange(0, 1000000)
        salary_input.setSingleStep(1000)
        email_input = QtWidgets.QLineEdit()
        address_input = QtWidgets.QLineEdit()
        phone_input = QtWidgets.QLineEdit()
        date_start_input = QtWidgets.QDateEdit()
        date_start_input.setCalendarPopup(True)
        date_start_input.setDate(QtCore.QDate.currentDate())

        # Добавляем поля в форму
        layout.addRow("Отель:", hotel_input)
        layout.addRow("Имя:", name_input)
        layout.addRow("Фамилия:", surname_input)
        layout.addRow("Должность:", type_input)
        layout.addRow("Зарплата:", salary_input)
        layout.addRow("Email:", email_input)
        layout.addRow("Адрес:", address_input)
        layout.addRow("Телефон:", phone_input)
        layout.addRow("Дата начала работы:", date_start_input)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        dialog.setLayout(layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                with PGSession() as session:
                    new_worker = Worker(
                        hotel_id=hotel_dict[hotel_input.currentText()],
                        name=name_input.text(),
                        surname=surname_input.text(),
                        type=type_input.currentText(),
                        salary=salary_input.value(),
                        email=email_input.text(),
                        address=address_input.text(),
                        phone=phone_input.text(),
                        date_start=date_start_input.date().toPyDate(),
                        is_active=True
                    )
                    session.add(new_worker)
                    session.commit()
                    self.load_employees()  # Обновляем таблицу
                    QtWidgets.QMessageBox.information(self, "Успех", "Работник успешно добавлен")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении работника: {str(e)}")

    def delete_employee(self):
        """Удаление работника (установка is_active = False)"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите работника для удаления")
            return

        row = selected_items[0].row()
        employee_id = int(self.table.item(row, 0).text())
        
        reply = QtWidgets.QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить работника с ID {employee_id}?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                with PGSession() as session:
                    worker = session.execute(
                        select(Worker).where(Worker.id == employee_id)
                    ).scalar_one()
                    
                    if worker:
                        worker.is_active = False
                        session.commit()
                        self.load_employees()  # Обновляем таблицу после удаления
                        QtWidgets.QMessageBox.information(self, "Успех", f"Работник с ID {employee_id} деактивирован")
                    else:
                        QtWidgets.QMessageBox.warning(self, "Ошибка", "Работник не найден")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении работника: {str(e)}")

    def update_salary(self):
        """Изменение зарплаты работника"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите работника для изменения зарплаты")
            return

        try:
            row = selected_items[0].row()
            employee_id = int(self.table.item(row, 0).text())
            # Сначала преобразуем в float, затем округляем до целого
            current_salary = round(float(self.table.item(row, 5).text()))

            new_salary, ok = QtWidgets.QInputDialog.getInt(
                self, 
                "Изменение зарплаты",
                "Введите новую зарплату:",
                current_salary,
                0,
                1000000,
                1
            )

            if ok:
                with PGSession() as session:
                    worker = session.execute(
                        select(Worker).where(Worker.id == employee_id)
                    ).scalar_one()
                    
                    if worker:
                        worker.salary = new_salary
                        session.commit()
                        self.load_employees()  # Обновляем таблицу
                        QtWidgets.QMessageBox.information(self, "Успех", f"Зарплата работника обновлена до {new_salary}")
                    else:
                        QtWidgets.QMessageBox.warning(self, "Ошибка", "Работник не найден")
        except ValueError as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Неверный формат зарплаты")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении зарплаты: {str(e)}")

app = QtWidgets.QApplication([])

login_window = LoginWindow()
login_window.show()

app.exec_()

