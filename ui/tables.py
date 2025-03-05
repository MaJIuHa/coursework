from PyQt5 import QtWidgets, QtGui
from db.core import PGSession
from db.models import Client, Booking, Room, Hotel, Review
from sqlalchemy import select

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
