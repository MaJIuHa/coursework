from PyQt5 import QtWidgets, QtGui
from db.core import PGSession
from db.models import Hotel, Room, Users
from ui.windows import StaffManagementWindow, SystemSettingsWindow, ReportsWindow
from ui.tables import RoomTable, BookingTable, ClientTable, HotelTable, ReviewTable
from sqlalchemy import select

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
