from PyQt5 import QtWidgets, QtGui, QtCore
from sqlalchemy import create_engine, Column, Integer, String, func, select
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, date


from ui.login import LoginWindow


app = QtWidgets.QApplication([])

login_window = LoginWindow()
login_window.show()

app.exec_()

