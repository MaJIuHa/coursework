import datetime
import enum
from typing import List, Optional
from db.base import Base

from sqlalchemy import Column, Integer, String, Float, Text, Boolean, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Hotel(Base):
    __tablename__ = 'hotel'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    coordinates: Mapped[List[float]] = mapped_column(ARRAY(Float))
    rating: Mapped[int] = mapped_column(Float)
    description: Mapped[str] = mapped_column(Text)
    contacts: Mapped[str] = mapped_column(String)
    rooms: Mapped[List["Room"]] = relationship("Room", back_populates="hotel")
    workers: Mapped[List["Worker"]] = relationship("Worker", back_populates="hotel")
    services: Mapped[List["Service"]] = relationship("Service", back_populates="hotel")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="hotel")

class RoomType(enum.Enum):

    SINGLE = 'одноместный' 
    DUO = 'двухместный' 
    TRIPLE = 'трехместный'
    QUADRUPLE = 'четырехместный'

class Room(Base):
    __tablename__ = 'room'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hotel_id: Mapped[Optional[int]] = mapped_column(Integer, 
        ForeignKey("public.hotel.id"))
    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates="rooms")
    type: Mapped[RoomType] = mapped_column(String)
    cost: Mapped[int] = mapped_column(Integer)
    capacity: Mapped[int] = mapped_column(Integer)
    other_services: Mapped[List[str]] = mapped_column(ARRAY(String))
    is_free: Mapped[bool] = mapped_column(Boolean)
    
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="room")

class Client(Base):
    __tablename__ = 'client'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    date_birthday: Mapped[datetime.date] = mapped_column(Date)
    passport: Mapped[str] = mapped_column(String)
    

    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="client")
    service_purchases: Mapped[List["ServicePurchase"]] = relationship("ServicePurchase", back_populates="client")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="client")

class WorkerType(enum.Enum):
    ADMIN = 'Администратор' 
    MANAGER = 'Менеджер' 
    CLEANER = 'Уборщик'
    ENGINER = 'Технический специалист'
    
class BookingStatus(enum.Enum):
    DECORATED = 'Оформлен' 
    CONFIRMED = 'Подтвержден' 
    CANCELED = 'Отменен'
    FINISHED = 'Завершен'

class Worker(Base):
    __tablename__ = 'worker'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hotel_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("public.hotel.id"))
    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates="workers")
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    type: Mapped[WorkerType] = mapped_column(String)
    salary: Mapped[float] = mapped_column(Float)
    email: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    date_start: Mapped[datetime.date] = mapped_column(Date)
    date_end: Mapped[datetime.date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean)

    def short_dict(self) -> dict:
        return dict(
            id=self.id,
            hotel_id=self.hotel_id,
            name=self.name,
            surname=self.surname,
            type=self.type,
            salary=self.salary,
            email=self.email,
            address=self.address,
            phone=self.phone,
            date_start=self.date_start.strftime('%d.%m.%Y') if self.date_start else None,
            date_end=self.date_end.strftime('%d.%m.%Y')  if self.date_end else None,
            is_activae=self.is_active
        )

class Service(Base):
    __tablename__ = 'service'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hotel_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("public.hotel.id"))
    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates="services")
    title: Mapped[str] = mapped_column(String)
    cost: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    
    service_purchases: Mapped[List["ServicePurchase"]] = relationship("ServicePurchase", back_populates="service")

class ServicePurchase(Base):
    __tablename__ = 'service_purchase'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("public.client.id"))
    client: Mapped["Client"] = relationship("Client", back_populates="service_purchases")
    service_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("public.service.id"))
    service: Mapped["Service"] = relationship("Service", back_populates="service_purchases")
    date: Mapped[datetime.date] = mapped_column(Date)
    total_sum: Mapped[float] = mapped_column(Float)

class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("public.client.id"))
    client: Mapped["Client"] = relationship("Client", back_populates="reviews")
    hotel_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("public.hotel.id"))
    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates="reviews")
    rating: Mapped[int] = mapped_column(Integer)
    commentary: Mapped[str] = mapped_column(Text)
    date_add: Mapped[datetime.date] = mapped_column(Date)
    moderated: Mapped[bool] = mapped_column(Boolean)

class Booking(Base):
    __tablename__ = 'booking'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("public.client.id"))
    client: Mapped["Client"] = relationship("Client", back_populates="bookings")
    room_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("public.room.id"))
    room: Mapped["Room"] = relationship("Room", back_populates="bookings")
    status: Mapped[BookingStatus] = mapped_column(String)
    date_start: Mapped[datetime.date] = mapped_column(Date)
    date_end: Mapped[datetime.date] = mapped_column(Date)
    total_sum: Mapped[float] = mapped_column(Float)
    
    def short_dict(self) -> dict:
        return dict(
            id=self.id,
            client_id=self.client_id,
            room_id=self.room_id,
            status=self.status,
            date_start=self.date_start.strftime('%d.%m.%Y'),
            date_end=self.date_end.strftime('%d.%m.%Y'),
            total_sum=self.total_sum,
        )

