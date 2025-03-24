from PyQt5 import QtWidgets, QtGui
from dotenv import load_dotenv
from db.core import PGSession
from db.models import Hotel, Room, Users, Client, Booking, Worker, Review
from ui.windows import StaffManagementWindow, SystemSettingsWindow, ReportsWindow
from ui.tables import RoomTable, BookingTable, ClientTable, HotelTable, ReviewTable
from sqlalchemy import select
import csv
import os
from datetime import datetime
import tempfile

from utils import upload_to_yadisk

load_dotenv('db/.env')

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

        # Кнопка экспорта
        export_button = QtWidgets.QPushButton("Экспорт данных")
        export_button.setFont(QtGui.QFont("Arial", 12))
        export_button.clicked.connect(self.show_export_menu)
        layout.addWidget(export_button)

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

    def show_export_menu(self):
        """Показывает диалог выбора способа экспорта"""
        export_types = ["Локальный экспорт", "Экспорт в Яндекс.Диск"]
        export_type, ok = QtWidgets.QInputDialog.getItem( 
            self,
            "Выбор способа экспорта",
            "Выберите способ экспорта:",
            export_types,
            0,
            False
        )
        
        if ok:
            use_yadisk = export_type == "Экспорт в Яндекс.Диск"
            
            # Диалог выбора количества таблиц
            table_types = ["Одна таблица", "Все таблицы"]
            table_type, ok = QtWidgets.QInputDialog.getItem(
                self,
                "Выбор таблиц",
                "Выберите, что экспортировать:",
                table_types,
                0,
                False
            )
            
            if ok:
                if table_type == "Одна таблица":
                    self.export_data(use_yadisk=use_yadisk)
                else:
                    self.export_all_data(use_yadisk=use_yadisk)



    def export_data(self, use_yadisk=False):
        """Экспорт данных в CSV"""
        tables = {
            "Отели": Hotel,
            "Номера": Room,
            "Клиенты": Client,
            "Бронирования": Booking,
            "Работники": Worker,
            "Отзывы": Review,
            "Пользователи": Users
        }
        
        # Диалог выбора таблицы
        table_name, ok = QtWidgets.QInputDialog.getItem(
            self,
            "Выбор таблицы",
            "Выберите таблицу для экспорта:",
            tables.keys(),
            0,
            False
        )
        
        if ok and table_name:
            try:
                with PGSession() as session:
                    # Получаем данные из выбранной таблицы
                    data = session.execute(select(tables[table_name])).scalars().all()
                    
                    if not data:
                        QtWidgets.QMessageBox.warning(self, "Предупреждение", "Таблица пуста")
                        return
                    
                    # Создаем временный файл
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{table_name}_{timestamp}.csv"
                    
                    if use_yadisk:
                        # Создаем временный файл
                        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8-sig') as temp_file:
                            # Получаем все атрибуты объекта, исключая служебные
                            sample_dict = vars(data[0])
                            fieldnames = [key for key in sample_dict.keys() if not key.startswith('_')]
                            
                            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
                            writer.writeheader()
                            
                            for item in data:
                                # Преобразуем объект в словарь и удаляем служебные атрибуты
                                row_dict = {k: v for k, v in vars(item).items() if not k.startswith('_')}
                                writer.writerow(row_dict)
                            
                            temp_file_path = temp_file.name
                        
                        # Загружаем на Яндекс.Диск
                        if upload_to_yadisk(temp_file_path, f"/hotel_data/{filename}", os.getenv("OAUTH_YANDEX_API")):
                            QtWidgets.QMessageBox.information(
                                self,
                                "Успех",
                                f"Данные успешно экспортированы на Яндекс.Диск в файл {filename}"
                            )
                        
                        # Удаляем временный файл
                        os.unlink(temp_file_path)
                    else:
                        # Локальное сохранение
                        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                            self,
                            "Сохранить файл",
                            filename,
                            "CSV Files (*.csv)"
                        )
                        
                        if file_path:
                            # Получаем все атрибуты объекта, исключая служебные
                            sample_dict = vars(data[0])
                            fieldnames = [key for key in sample_dict.keys() if not key.startswith('_')]
                            
                            with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writeheader()
                                
                                for item in data:
                                    # Преобразуем объект в словарь и удаляем служебные атрибуты
                                    row_dict = {k: v for k, v in vars(item).items() if not k.startswith('_')}
                                    writer.writerow(row_dict)
                            
                            QtWidgets.QMessageBox.information(
                                self,
                                "Успех",
                                f"Данные успешно экспортированы в {file_path}"
                            )
            
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Ошибка",
                    f"Произошла ошибка при экспорте данных: {str(e)}"
                )

    def export_all_data(self, use_yadisk=False):
        """Экспорт всех таблиц в CSV"""
        tables = {
            "hotels": Hotel,
            "rooms": Room,
            "clients": Client,
            "bookings": Booking,
            "workers": Worker,
            "reviews": Review,
            "users": Users
        }
        
        try:
            if use_yadisk:
                # Создаем временную директорию
                with tempfile.TemporaryDirectory() as temp_dir:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    exported_tables = 0
                    
                    with PGSession() as session:
                        for table_name, model in tables.items():
                            data = session.execute(select(model)).scalars().all()
                            if data:
                                # Создаем временный файл
                                filename = f"{table_name}_{timestamp}.csv"
                                temp_file_path = os.path.join(temp_dir, filename)
                                
                                # Получаем все атрибуты объекта, исключая служебные
                                sample_dict = vars(data[0])
                                fieldnames = [key for key in sample_dict.keys() if not key.startswith('_')]
                                
                                with open(temp_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                    writer.writeheader()
                                    
                                    for item in data:
                                        # Преобразуем объект в словарь и удаляем служебные атрибуты
                                        row_dict = {k: v for k, v in vars(item).items() if not k.startswith('_')}
                                        writer.writerow(row_dict)
                                
                                # Загружаем на Яндекс.Диск
                                if upload_to_yadisk(temp_file_path, f"/hotel_data/{filename}", os.getenv("OAUTH_YANDEX_API")):
                                    exported_tables += 1
                
                if exported_tables > 0:
                    QtWidgets.QMessageBox.information(
                        self,
                        "Успех",
                        f"Экспортировано таблиц: {exported_tables}\nВсе файлы загружены в папку /hotel_data на Яндекс.Диске"
                    )
                else:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Предупреждение",
                        "Нет данных для экспорта"
                    )
            else:
                # Локальное сохранение
                export_dir = QtWidgets.QFileDialog.getExistingDirectory(
                    self,
                    "Выберите папку для экспорта"
                )
                
                if export_dir:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    exported_tables = 0
                    
                    with PGSession() as session:
                        for table_name, model in tables.items():
                            data = session.execute(select(model)).scalars().all()
                            if data:
                                # Создаем имя файла
                                file_path = os.path.join(export_dir, f"{table_name}_{timestamp}.csv")
                                
                                # Получаем все атрибуты объекта, исключая служебные
                                sample_dict = vars(data[0])
                                fieldnames = [key for key in sample_dict.keys() if not key.startswith('_')]
                                
                                with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
                                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                    writer.writeheader()
                                    
                                    for item in data:
                                        # Преобразуем объект в словарь и удаляем служебные атрибуты
                                        row_dict = {k: v for k, v in vars(item).items() if not k.startswith('_')}
                                        writer.writerow(row_dict)
                                
                                exported_tables += 1
                    
                    if exported_tables > 0:
                        QtWidgets.QMessageBox.information(
                            self,
                            "Успех",
                            f"Экспортировано таблиц: {exported_tables}\nПуть: {export_dir}"
                        )
                    else:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "Предупреждение",
                            "Нет данных для экспорта"
                        )
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка при экспорте данных: {str(e)}"
            )

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
