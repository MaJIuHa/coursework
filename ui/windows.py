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
            # Упрощаем запрос, убираем лишние данные
            bookings = session.execute(
                select(
                    Booking.id,
                    Room.cost,
                    Booking.date_start,
                    Booking.date_end,
                    Booking.status
                )
                .select_from(Booking)
                .join(Room, Room.id == Booking.room_id)
                .where(
                    Booking.date_start >= start_date,
                    Booking.date_end <= end_date
                )
            ).all()

            # Очищаем таблицу
            self.table.setRowCount(0)
            total_revenue = 0

            # Обновляем заголовки таблицы
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(["Номер", "Даты", "Статус", "Стоимость"])

            # Заполняем таблицу данными
            for row, (booking_id, cost, date_start, date_end, status) in enumerate(bookings):
                self.table.insertRow(row)
                self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking_id)))
                self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(f"{date_start.strftime('%d.%m.%Y')} - {date_end.strftime('%d.%m.%Y')}"))
                self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(status))
                self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(f"{cost} руб."))
                
                total_revenue += cost

            # Обновляем label с общей суммой
            self.total_label.setText(f"Общая выручка: {total_revenue} руб.")

            # Если нет данных, показываем сообщение
            if not bookings:
                QtWidgets.QMessageBox.information(self, "Информация", "За выбранный период нет бронирований")

class StaffManagementWindow(QtWidgets.QWidget):