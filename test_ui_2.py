from PyQt5 import QtWidgets, QtGui, QtCore
from sqlalchemy import create_engine, Column, Integer, String, func, select
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, date

from db.core import PGSession

from typing import List

from db.models import Hotel, Room, Users, Review, Client, Booking, Worker, WorkerType


class SuperAdminPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Супер Админ Панель")
        self.setGeometry(100, 100, 500, 400)

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Супер Админ - Полный доступ")
        label.setFont(QtGui.QFont("Arial", 15))
        layout.addWidget(label)

        # Кнопка для управления персоналом
        staff_button = QtWidgets.QPushButton("Управление персоналом")
        staff_button.setFont(QtGui.QFont("Arial", 12))
        staff_button.clicked.connect(self.manage_staff)
        layout.addWidget(staff_button)

        settings_button = QtWidgets.QPushButton("Настройки системы")
        settings_button.setFont(QtGui.QFont("Arial", 12))
        settings_button.clicked.connect(self.open_system_settings)
        layout.addWidget(settings_button)

        reports_button = QtWidgets.QPushButton("Просмотр отчетов")
        reports_button.setFont(QtGui.QFont("Arial", 12))
        reports_button.clicked.connect(self.view_reports)
        layout.addWidget(reports_button)

        update_price_button = QtWidgets.QPushButton("Обновить цены номеров")
        update_price_button.setFont(QtGui.QFont("Arial", 12))
        update_price_button.clicked.connect(self.update_room_price)
        layout.addWidget(update_price_button)

        delete_user_button = QtWidgets.QPushButton("Удалить пользователя")
        delete_user_button.setFont(QtGui.QFont("Arial", 12))
        delete_user_button.clicked.connect(self.delete_user)
        layout.addWidget(delete_user_button)

        self.setLayout(layout)

    def manage_staff(self):
        self.staff_window = StaffManagementWindow()
        self.staff_window.show()

    def open_system_settings(self):
        self.settings_window = SystemSettingsWindow()
        self.settings_window.show()

    def view_reports(self):
        self.reports_window = ReportsWindow()
        self.reports_window.show()

    def view_users(self):
        with PGSession() as session:
            users = session.execute(select(Users)).scalars().all()
            for user in users:
                print(f"ID: {user.user_id}, Логин: {user.login}, Роль: {user.role}")

    def view_hotels(self):
        with PGSession() as session:
            hotels = session.execute(select(Hotel)).scalars().all()
            for hotel in hotels:
                print(f"ID: {hotel.id}, Название: {hotel.title}")

    def delete_user(self):
        username, ok = QtWidgets.QInputDialog.getText(self, "Удаление пользователя", "Введите логин пользователя для удаления:")
        if ok:
            with PGSession() as session:
                user = session.execute(select(Users).where(Users.login == username)).scalars().first()
                if user:
                    session.delete(user)
                    session.commit()
                    QtWidgets.QMessageBox.information(self, "Успех", f"Пользователь {username} удалён")
                else:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
    
    def update_room_price(self):
        room_id, ok = QtWidgets.QInputDialog.getInt(self, "Обновление цены", "Введите ID номера:")
        if ok:
            new_price, ok = QtWidgets.QInputDialog.getInt(self, "Обновление цены", "Введите новую цену:")
            if ok:
                with PGSession() as session:
                    room = session.execute(select(Room).where(Room.id == room_id)).scalars().first()
                    if room:
                        room.cost = new_price
                        session.commit()
                        QtWidgets.QMessageBox.information(self, "Успех", f"Цена номера {room_id} обновлена до {new_price}")
                    else:
                        QtWidgets.QMessageBox.warning(self, "Ошибка", "Номер не найден")






class AdminPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Админ Панель")
        self.setGeometry(100, 100, 500, 400)

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Админ - Частичное редактирование")
        label.setFont(QtGui.QFont("Arial", 15))
        layout.addWidget(label)

    

        view_clients_button = QtWidgets.QPushButton("Просмотр клиентов")
        view_clients_button.setFont(QtGui.QFont("Arial", 12))
        view_clients_button.clicked.connect(self.view_clients)
        layout.addWidget(view_clients_button)

        view_bookings_button = QtWidgets.QPushButton("Просмотр бронирований")
        view_bookings_button.setFont(QtGui.QFont("Arial", 12))
        view_bookings_button.clicked.connect(self.view_bookings)
        layout.addWidget(view_bookings_button)

        view_rooms_button = QtWidgets.QPushButton("Просмотр номеров")
        view_rooms_button.setFont(QtGui.QFont("Arial", 12))
        view_rooms_button.clicked.connect(self.view_rooms)
        layout.addWidget(view_rooms_button)

        self.setLayout(layout)

    def view_hotels(self):
        with PGSession() as session:
            stmt = select(Hotel)
            hotels = session.execute(stmt).scalars().all()
            for hotel in hotels:
                print(f"ID: {hotel.id}, Название: {hotel.title}")

    
    def view_clients(self):
        self.client_table = ClientTable()
        self.client_table.show()

    def view_bookings(self):
        self.booking_table = BookingTable()
        self.booking_table.show()

    def view_rooms(self):
        self.room_table = RoomTable()
        self.room_table.show()




class HotelTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список Отелей")
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)

        back_button = QtWidgets.QPushButton("Назад")
        back_button.setFont(QtGui.QFont("Arial", 12))
        back_button.clicked.connect(self.close)  # Закрывает текущее окно
        layout.addWidget(back_button)

        self.setLayout(layout)

        self.load_hotels()

    def load_hotels(self):
        with PGSession() as session:
            hotels = session.execute(select(Hotel)).scalars().all()
            self.table.setRowCount(len(hotels))
            self.table.setColumnCount(6)  # Количество столбцов без связей many-to-many
            self.table.setHorizontalHeaderLabels(["ID", "Название", "Координаты", "Рейтинг", "Описание", "Контакты"])

            for row, hotel in enumerate(hotels):
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(hotel.id)))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(hotel.title))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(hotel.coordinates)))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(hotel.rating)))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(hotel.description))
                self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(hotel.contacts))

class ReviewTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список Отзывов")
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)

        back_button = QtWidgets.QPushButton("Назад")
        back_button.setFont(QtGui.QFont("Arial", 12))
        back_button.clicked.connect(self.close)  # Закрывает текущее окно
        layout.addWidget(back_button)

        self.setLayout(layout)

        self.load_reviews()

    def load_reviews(self):
        with PGSession() as session:
            reviews = session.execute(
                select(Hotel.title, Room.cost, Review.commentary)
                .join(Hotel, Review.hotel_id == Hotel.id)
                .join(Room, Room.hotel_id == Hotel.id)
            ).all()

            self.table.setRowCount(len(reviews))
            self.table.setColumnCount(3)  # Количество столбцов: Название, Цена, Комментарий
            self.table.setHorizontalHeaderLabels(["Название", "Цена", "Комментарий"])

            for row, (hotel_title, room_cost, commentary) in enumerate(reviews):
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(hotel_title))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(room_cost)))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(commentary))

class UserPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Пользовательская Панель")
        self.setGeometry(100, 100, 500, 400)

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Пользователь - Только просмотр")
        label.setFont(QtGui.QFont("Arial", 15))
        layout.addWidget(label)

        view_hotels_button = QtWidgets.QPushButton("Просмотр отелей")
        view_hotels_button.setFont(QtGui.QFont("Arial", 12))
        view_hotels_button.clicked.connect(self.view_hotels)
        layout.addWidget(view_hotels_button)

        view_reviews_button = QtWidgets.QPushButton("Просмотр отзывов")
        view_reviews_button.setFont(QtGui.QFont("Arial", 12))
        view_reviews_button.clicked.connect(self.view_reviews)
        layout.addWidget(view_reviews_button)

        self.setLayout(layout)

    def view_hotels(self):
        self.hotel_table = HotelTable()
        self.hotel_table.show()

    def view_reviews(self):
        self.review_table = ReviewTable()
        self.review_table.show()

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

class ClientTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список Клиентов")
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)

        back_button = QtWidgets.QPushButton("Назад")
        back_button.setFont(QtGui.QFont("Arial", 12))
        back_button.clicked.connect(self.close)  # Закрывает текущее окно
        layout.addWidget(back_button)

        self.setLayout(layout)

        self.load_clients()

    def load_clients(self):
        with PGSession() as session:
            clients = session.execute(select(Client)).scalars().all()
            self.table.setRowCount(len(clients))
            self.table.setColumnCount(7)  # Количество столбцов для отображения информации о клиентах
            self.table.setHorizontalHeaderLabels(["ID", "Имя", "Фамилия", "Email", "Телефон", "Дата рождения", "Паспорт"])

            for row, client in enumerate(clients):
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(client.id)))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(client.name))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(client.surname))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(client.email))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(client.phone))
                self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(client.date_birthday.strftime('%d.%m.%Y')))
                self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(client.passport))

class BookingTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список Бронирований")
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)

        back_button = QtWidgets.QPushButton("Назад")
        back_button.setFont(QtGui.QFont("Arial", 12))
        back_button.clicked.connect(self.close)  # Закрывает текущее окно
        layout.addWidget(back_button)

        self.setLayout(layout)

        self.load_bookings()

    def load_bookings(self):
        with PGSession() as session:
            bookings = session.execute(select(Booking)).scalars().all()
            self.table.setRowCount(len(bookings))
            self.table.setColumnCount(7)  # Количество столбцов для отображения информации о бронированиях
            self.table.setHorizontalHeaderLabels(["ID", "Клиент ID", "Номер ID", "Статус", "Дата начала", "Дата окончания", "Сумма"])

            for row, booking in enumerate(bookings):
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking.id)))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(booking.client_id)))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(booking.room_id)))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(booking.status))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(booking.date_start.strftime('%d.%m.%Y')))
                self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(booking.date_end.strftime('%d.%m.%Y')))
                self.table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(booking.total_sum)))

class RoomTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список Номеров")
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)

        back_button = QtWidgets.QPushButton("Назад")
        back_button.setFont(QtGui.QFont("Arial", 12))
        back_button.clicked.connect(self.close)  # Закрывает текущее окно
        layout.addWidget(back_button)

        self.setLayout(layout)

        self.load_rooms()

    def load_rooms(self):
        with PGSession() as session:
            rooms = session.execute(select(Room)).scalars().all()
            self.table.setRowCount(len(rooms))
            self.table.setColumnCount(7)  # Количество столбцов для отображения информации о номерах
            self.table.setHorizontalHeaderLabels(["ID", "Отель ID", "Тип", "Цена", "Вместимость", "Услуги", "Свободен"])

            for row, room in enumerate(rooms):
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(room.id)))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(room.hotel_id)))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(room.type))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(room.cost)))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(room.capacity)))
                self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(", ".join(room.other_services)))
                self.table.setItem(row, 6, QtWidgets.QTableWidgetItem("Да" if room.is_free else "Нет"))

class SystemSettingsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Настройки системы")
        self.setGeometry(150, 150, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        # Создаем вкладки с увеличенным размером
        tabs = QtWidgets.QTabWidget()
        tabs.setFont(QtGui.QFont("Arial", 12))  # Увеличиваем шрифт вкладок
        tabs.setStyleSheet("""
            QTabBar::tab {
                min-width: 100px;
                min-height: 20px;
                padding: 5px;
                margin: 2px;
                background-color: #f0f0f0;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #e0e0e0;
                border-bottom: 2px solid #0078d7;
            }
            QTabBar::tab:hover {
                background-color: #e5e5e5;
            }
        """)

        # Вкладка Отели
        hotels_tab = QtWidgets.QWidget()
        hotels_layout = QtWidgets.QVBoxLayout()
        
        self.hotels_table = QtWidgets.QTableWidget()
        self.hotels_table.setColumnCount(6)
        self.hotels_table.setHorizontalHeaderLabels(["ID", "Название", "Координаты", "Рейтинг", "Описание", "Контакты"])
        hotels_layout.addWidget(self.hotels_table)
        
        hotels_buttons = QtWidgets.QHBoxLayout()
        add_hotel_btn = QtWidgets.QPushButton("Добавить отель")
        edit_hotel_btn = QtWidgets.QPushButton("Редактировать")
        delete_hotel_btn = QtWidgets.QPushButton("Удалить")
        
        add_hotel_btn.clicked.connect(self.add_hotel)
        edit_hotel_btn.clicked.connect(self.edit_hotel)
        delete_hotel_btn.clicked.connect(self.delete_hotel)
        
        hotels_buttons.addWidget(add_hotel_btn)
        hotels_buttons.addWidget(edit_hotel_btn)
        hotels_buttons.addWidget(delete_hotel_btn)
        hotels_layout.addLayout(hotels_buttons)
        
        hotels_tab.setLayout(hotels_layout)
        
        # Вкладка Номера
        rooms_tab = QtWidgets.QWidget()
        rooms_layout = QtWidgets.QVBoxLayout()
        
        self.rooms_table = QtWidgets.QTableWidget()
        self.rooms_table.setColumnCount(7)
        self.rooms_table.setHorizontalHeaderLabels(["ID", "Отель", "Тип", "Цена", "Вместимость", "Услуги", "Свободен"])
        rooms_layout.addWidget(self.rooms_table)
        
        rooms_buttons = QtWidgets.QHBoxLayout()
        add_room_btn = QtWidgets.QPushButton("Добавить номер")
        edit_room_btn = QtWidgets.QPushButton("Редактировать")
        delete_room_btn = QtWidgets.QPushButton("Удалить")
        
        add_room_btn.clicked.connect(self.add_room)
        edit_room_btn.clicked.connect(self.edit_room)
        delete_room_btn.clicked.connect(self.delete_room)
        
        rooms_buttons.addWidget(add_room_btn)
        rooms_buttons.addWidget(edit_room_btn)
        rooms_buttons.addWidget(delete_room_btn)
        rooms_layout.addLayout(rooms_buttons)
        
        rooms_tab.setLayout(rooms_layout)
        
        # Добавляем вкладки
        tabs.addTab(hotels_tab, "Отели")
        tabs.addTab(rooms_tab, "Номера")
        
        layout.addWidget(tabs)
        self.setLayout(layout)
        
        # Загружаем данные
        self.load_hotels()
        self.load_rooms()

    def load_hotels(self):
        with PGSession() as session:
            hotels = session.execute(select(Hotel)).scalars().all()
            self.hotels_table.setRowCount(len(hotels))
            
            for row, hotel in enumerate(hotels):
                self.hotels_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(hotel.id)))
                self.hotels_table.setItem(row, 1, QtWidgets.QTableWidgetItem(hotel.title))
                self.hotels_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(hotel.coordinates)))
                self.hotels_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(hotel.rating)))
                self.hotels_table.setItem(row, 4, QtWidgets.QTableWidgetItem(hotel.description))
                self.hotels_table.setItem(row, 5, QtWidgets.QTableWidgetItem(hotel.contacts))

    def load_rooms(self):
        with PGSession() as session:
            rooms = session.execute(
                select(Room, Hotel.title)
                .join(Hotel, Room.hotel_id == Hotel.id)
            ).all()
            self.rooms_table.setRowCount(len(rooms))
            
            for row, (room, hotel_title) in enumerate(rooms):
                self.rooms_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(room.id)))
                self.rooms_table.setItem(row, 1, QtWidgets.QTableWidgetItem(hotel_title))
                self.rooms_table.setItem(row, 2, QtWidgets.QTableWidgetItem(room.type))
                self.rooms_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(room.cost)))
                self.rooms_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(room.capacity)))
                self.rooms_table.setItem(row, 5, QtWidgets.QTableWidgetItem(", ".join(room.other_services)))
                self.rooms_table.setItem(row, 6, QtWidgets.QTableWidgetItem("Да" if room.is_free else "Нет"))

    def add_hotel(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Добавление отеля")
        layout = QtWidgets.QFormLayout()

        title_input = QtWidgets.QLineEdit()
        coords_input = QtWidgets.QLineEdit()
        rating_input = QtWidgets.QSpinBox()
        rating_input.setRange(1, 5)
        description_input = QtWidgets.QTextEdit()
        contacts_input = QtWidgets.QLineEdit()

        layout.addRow("Название:", title_input)
        layout.addRow("Координаты (через запятую):", coords_input)
        layout.addRow("Рейтинг:", rating_input)
        layout.addRow("Описание:", description_input)
        layout.addRow("Контакты:", contacts_input)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        dialog.setLayout(layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                coords = [float(x.strip()) for x in coords_input.text().split(",")]
                with PGSession() as session:
                    new_hotel = Hotel(
                        title=title_input.text(),
                        coordinates=coords,
                        rating=rating_input.value(),
                        description=description_input.toPlainText(),
                        contacts=contacts_input.text()
                    )
                    session.add(new_hotel)
                    session.commit()
                    QtWidgets.QMessageBox.information(self, "Успех", "Отель успешно добавлен")
                    self.load_hotels()
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный формат координат")

    def edit_hotel(self):
        selected_items = self.hotels_table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите отель для редактирования")
            return

        hotel_id = int(self.hotels_table.item(selected_items[0].row(), 0).text())
        
        with PGSession() as session:
            hotel = session.execute(select(Hotel).where(Hotel.id == hotel_id)).scalar_one_or_none()
            if not hotel:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Отель не найден")
                return

            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Редактирование отеля")
            layout = QtWidgets.QFormLayout()

            title_input = QtWidgets.QLineEdit(hotel.title)
            coords_input = QtWidgets.QLineEdit(",".join(map(str, hotel.coordinates)))
            rating_input = QtWidgets.QSpinBox()
            rating_input.setRange(1, 5)
            rating_input.setValue(int(hotel.rating))
            description_input = QtWidgets.QTextEdit()
            description_input.setText(hotel.description)
            contacts_input = QtWidgets.QLineEdit(hotel.contacts)

            layout.addRow("Название:", title_input)
            layout.addRow("Координаты (через запятую):", coords_input)
            layout.addRow("Рейтинг:", rating_input)
            layout.addRow("Описание:", description_input)
            layout.addRow("Контакты:", contacts_input)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
                QtCore.Qt.Horizontal)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)

            dialog.setLayout(layout)

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                try:
                    coords = [float(x.strip()) for x in coords_input.text().split(",")]
                    hotel.title = title_input.text()
                    hotel.coordinates = coords
                    hotel.rating = rating_input.value()
                    hotel.description = description_input.toPlainText()
                    hotel.contacts = contacts_input.text()
                    session.commit()
                    QtWidgets.QMessageBox.information(self, "Успех", "Отель успешно обновлен")
                    self.load_hotels()
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный формат координат")

    def delete_hotel(self):
        selected_items = self.hotels_table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите отель для удаления")
            return

        hotel_id = int(self.hotels_table.item(selected_items[0].row(), 0).text())
        
        reply = QtWidgets.QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить этот отель?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            with PGSession() as session:
                hotel = session.execute(select(Hotel).where(Hotel.id == hotel_id)).scalar_one_or_none()
                if hotel:
                    session.delete(hotel)
                    session.commit()
                    QtWidgets.QMessageBox.information(self, "Успех", "Отель успешно удален")
                    self.load_hotels()
                else:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Отель не найден")

    # Аналогичные методы для работы с номерами
    def add_room(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Добавление номера")
        layout = QtWidgets.QFormLayout()

        # Получаем список отелей
        with PGSession() as session:
            hotels = session.execute(select(Hotel.id, Hotel.title)).all()
            hotel_dict = {hotel[1]: hotel[0] for hotel in hotels}

        hotel_input = QtWidgets.QComboBox()
        hotel_input.addItems(hotel_dict.keys())
        
        type_input = QtWidgets.QComboBox()
        type_input.addItems(["одноместный", "двухместный", "трехместный", "четырехместный"])
        
        cost_input = QtWidgets.QSpinBox()
        cost_input.setRange(0, 1000000)
        cost_input.setSingleStep(100)
        
        capacity_input = QtWidgets.QSpinBox()
        capacity_input.setRange(1, 10)
        
        services_input = QtWidgets.QLineEdit()
        
        layout.addRow("Отель:", hotel_input)
        layout.addRow("Тип:", type_input)
        layout.addRow("Стоимость:", cost_input)
        layout.addRow("Вместимость:", capacity_input)
        layout.addRow("Доп. услуги (через запятую):", services_input)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        dialog.setLayout(layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            with PGSession() as session:
                services = [s.strip() for s in services_input.text().split(",") if s.strip()]
                new_room = Room(
                    hotel_id=hotel_dict[hotel_input.currentText()],
                    type=type_input.currentText(),
                    cost=cost_input.value(),
                    capacity=capacity_input.value(),
                    other_services=services,
                    is_free=True
                )
                session.add(new_room)
                session.commit()
                QtWidgets.QMessageBox.information(self, "Успех", "Номер успешно добавлен")
                self.load_rooms()

    def edit_room(self):
        selected_items = self.rooms_table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите номер для редактирования")
            return

        room_id = int(self.rooms_table.item(selected_items[0].row(), 0).text())
        
        with PGSession() as session:
            room = session.execute(select(Room).where(Room.id == room_id)).scalar_one_or_none()
            if not room:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Номер не найден")
                return

            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Редактирование номера")
            layout = QtWidgets.QFormLayout()

            cost_input = QtWidgets.QSpinBox()
            cost_input.setRange(0, 1000000)
            cost_input.setSingleStep(100)
            cost_input.setValue(room.cost)
            
            services_input = QtWidgets.QLineEdit(", ".join(room.other_services))
            
            layout.addRow("Стоимость:", cost_input)
            layout.addRow("Доп. услуги (через запятую):", services_input)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
                QtCore.Qt.Horizontal)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)

            dialog.setLayout(layout)

            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                services = [s.strip() for s in services_input.text().split(",") if s.strip()]
                room.cost = cost_input.value()
                room.other_services = services
                session.commit()
                QtWidgets.QMessageBox.information(self, "Успех", "Номер успешно обновлен")
                self.load_rooms()

    def delete_room(self):
        selected_items = self.rooms_table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите номер для удаления")
            return

        room_id = int(self.rooms_table.item(selected_items[0].row(), 0).text())
        
        reply = QtWidgets.QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить этот номер?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            with PGSession() as session:
                room = session.execute(select(Room).where(Room.id == room_id)).scalar_one_or_none()
                if room:
                    session.delete(room)
                    session.commit()
                    QtWidgets.QMessageBox.information(self, "Успех", "Номер успешно удален")
                    self.load_rooms()
                else:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Номер не найден")

class ReportsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр отчетов")
        self.setGeometry(150, 150, 800, 600)  # Увеличим размер окна

        layout = QtWidgets.QVBoxLayout()

        # Поля для ввода дат
        dates_layout = QtWidgets.QHBoxLayout()
        
        date_widget = QtWidgets.QWidget()
        date_layout = QtWidgets.QVBoxLayout()
        
        self.start_date_edit = QtWidgets.QDateEdit(calendarPopup=True)
        self.start_date_edit.setDisplayFormat("dd.MM.yyyy")
        date_layout.addWidget(QtWidgets.QLabel("Дата начала:"))
        date_layout.addWidget(self.start_date_edit)

        self.end_date_edit = QtWidgets.QDateEdit(calendarPopup=True)
        self.end_date_edit.setDisplayFormat("dd.MM.yyyy")
        date_layout.addWidget(QtWidgets.QLabel("Дата окончания:"))
        date_layout.addWidget(self.end_date_edit)
        
        date_widget.setLayout(date_layout)
        dates_layout.addWidget(date_widget)
        
        # Кнопка для расчета выручки
        calculate_button = QtWidgets.QPushButton("Рассчитать выручку")
        calculate_button.setFont(QtGui.QFont("Arial", 12))
        calculate_button.clicked.connect(self.calculate_revenue)
        dates_layout.addWidget(calculate_button)
        
        layout.addLayout(dates_layout)

        # Таблица для отображения результатов
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Номер", "Даты", "Статус", "Стоимость", "Клиент"])
        layout.addWidget(self.table)

        # Поле для отображения общей суммы
        self.total_label = QtWidgets.QLabel("Общая выручка: 0 руб.")
        self.total_label.setFont(QtGui.QFont("Arial", 14))
        layout.addWidget(self.total_label)

        self.setLayout(layout)

    def calculate_revenue(self):
        start_date = self.start_date_edit.date().toPyDate()
        end_date = self.end_date_edit.date().toPyDate()

        with PGSession() as session:
            # Получаем информацию о бронированиях с ценами номеров
            bookings = session.execute(
                select(
                    Booking.id,
                    Room.cost,
                    Booking.date_start,
                    Booking.date_end,
                    Booking.status,
                    Client.name,
                    Client.surname
                )
                .select_from(Booking)
                .join(Room, Room.id == Booking.room_id)
                .join(Client, Client.id == Booking.client_id)
                .where(
                    Booking.date_start >= start_date,
                    Booking.date_end <= end_date
                )
            ).all()

            # Очищаем таблицу
            self.table.setRowCount(0)
            total_revenue = 0

            # Заполняем таблицу данными
            for row, (booking_id, cost, date_start, date_end, status, client_name, client_surname) in enumerate(bookings):
                # Вычисляем количество дней
                days = (date_end - date_start).days
                # Вычисляем стоимость за весь период
                period_cost = cost * days if days > 0 else cost
                
                self.table.insertRow(row)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking_id)))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{date_start.strftime('%d.%m.%Y')} - {date_end.strftime('%d.%m.%Y')}"))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(status))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{period_cost} руб. ({days} дн.)"))
                self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(f"{client_name} {client_surname}"))
                
                total_revenue += period_cost

            # Обновляем label с общей суммой
            self.total_label.setText(f"Общая выручка: {total_revenue} руб.")

            # Если нет данных, показываем сообщение
            if not bookings:
                QtWidgets.QMessageBox.information(self, "Информация", "За выбранный период нет бронирований")

class StaffManagementWindow(QtWidgets.QWidget):
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
                workers = session.execute(
                    select(Worker, Hotel.title)
                    .join(Hotel, Worker.hotel_id == Hotel.id)
                    .where(Worker.is_active == True)  # Показываем только активных работников
                ).all()
                
                self.table.setRowCount(0)  # Очищаем таблицу перед заполнением
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
                    self.table.setItem(row, 10, QtWidgets.QTableWidgetItem(
                        worker.date_end.strftime('%d.%m.%Y') if worker.date_end else '-'
                    ))
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке списка работников: {str(e)}")

    def add_employee(self):
        """Добавление нового работника"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Добавление работника")
        layout = QtWidgets.QFormLayout()

        with PGSession() as session:
            hotels = session.execute(select(Hotel.id, Hotel.title)).all()
            hotel_dict = {hotel[1]: hotel[0] for hotel in hotels}

        hotel_input = QtWidgets.QComboBox()
        hotel_input.addItems(hotel_dict.keys())
        name_input = QtWidgets.QLineEdit()
        surname_input = QtWidgets.QLineEdit()
        
        # Исправляем список должностей
        type_input = QtWidgets.QComboBox()
        worker_types = ["Администратор", "Менеджер", "Уборщик", "Технический специалист"]
        type_input.addItems(worker_types)
        
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
                    self.load_employees()
                    QtWidgets.QMessageBox.information(self, "Успех", "Работник успешно добавлен")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении работника: {str(e)}")

    def delete_employee(self):
        """Удаление работника (установка is_active = False)"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            QtWidgets.QMessageBox.warning(self, "Предупреждение", "Выберите работника для удаления")
            return

        employee_id = int(self.table.item(selected_items[0].row(), 0).text())
        
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
                        worker.date_end = datetime.now().date()
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

        employee_id = int(self.table.item(selected_items[0].row(), 0).text())
        current_salary = float(self.table.item(selected_items[0].row(), 5).text())

        new_salary, ok = QtWidgets.QInputDialog.getDouble(
            self, 
            "Изменение зарплаты",
            "Введите новую зарплату:",
            current_salary,
            0,
            1000000,
            2
        )

        if ok:
            try:
                with PGSession() as session:
                    worker = session.execute(
                        select(Worker).where(
                            Worker.id == employee_id,
                            Worker.is_active == True
                        )
                    ).scalar_one_or_none()
                    
                    if worker:
                        worker.salary = float(new_salary)  # Преобразуем в float
                        session.commit()
                        QtWidgets.QMessageBox.information(self, "Успех", f"Зарплата работника обновлена до {new_salary}")
                        self.load_employees()
                    else:
                        QtWidgets.QMessageBox.warning(self, "Ошибка", "Работник не найден")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении зарплаты: {str(e)}")

app = QtWidgets.QApplication([])

login_window = LoginWindow()
login_window.show()

app.exec_()
