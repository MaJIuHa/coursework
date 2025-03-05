import asyncio 
from db.core import PGSession 
from faker import Faker 
import random 
from db.models import Base, Hotel, Room, Client, Worker, Service, ServicePurchase, Review, Booking, RoomType, WorkerType, BookingStatus 
 
fake = Faker() 
 
def generate_data(): 
    with PGSession() as session: 
        hotels = [] 
        for _ in range(1000): 
            hotel = Hotel( 
                title=fake.company(), 
                coordinates=[fake.latitude(), fake.longitude()], 
                rating=random.uniform(1, 5), 
                description=fake.text(), 
                contacts=fake.phone_number() 
            ) 
            hotels.append(hotel) 
        session.add_all(hotels) 
        session.commit() 
 
        clients = [] 
        for _ in range(1000): 
            client = Client( 
                name=fake.first_name(), 
                surname=fake.last_name(), 
                email=fake.email(), 
                phone=fake.phone_number(), 
                date_birthday=fake.date_of_birth(), 
                passport=fake.ssn() 
            ) 
            clients.append(client) 
        session.add_all(clients) 
        session.commit() 
 
        rooms = [] 
        for hotel in hotels: 
            for _ in range(10):  
                room = Room( 
                    hotel_id=hotel.id, 
                    type=random.choice(list(RoomType)).value, 
                    cost=random.randint(50, 500), 
                    capacity=random.randint(1, 4), 
                    other_services=[fake.word() for _ in range(3)], 
                    is_free=random.choice([True, False]) 
                ) 
                rooms.append(room) 
        session.add_all(rooms) 
        session.commit() 
 
        workers = [] 
        for hotel in hotels: 
            for _ in range(5): 
                worker = Worker( 
                    hotel_id=hotel.id, 
                    name=fake.first_name(), 
                    surname=fake.last_name(), 
                    type=random.choice(list(WorkerType)).value, 
                    salary=random.uniform(30000, 100000), 
                    email=fake.email(), 
                    address=fake.address(), 
                    phone=fake.phone_number(), 
                    date_start=fake.date_this_decade(), 
                    date_end=fake.date_this_decade(), 
                    is_active=random.choice([True, False]) 
                ) 
                workers.append(worker) 
        session.add_all(workers) 
        session.commit() 
 
        services = [] 
        for hotel in hotels: 
            for _ in range(5): 
                service = Service( 
                    hotel_id=hotel.id, 
                    title=fake.word(), 
                    cost=random.randint(10, 100), 
                    description=fake.text() 
                ) 
                services.append(service) 
        session.add_all(services) 
        session.commit() 
 
        service_purchases = [] 
        for _ in range(1000): 
            service_purchase = ServicePurchase( 
                client_id=random.choice(clients).id, 
                service_id=random.choice(services).id, 
                date=fake.date_this_year(), 
                total_sum=random.uniform(10, 100) 
            ) 
            service_purchases.append(service_purchase) 
        session.add_all(service_purchases) 
        session.commit() 
 
        reviews = [] 
        for _ in range(1000): 
            review = Review( 
                client_id=random.choice(clients).id, 
                hotel_id=random.choice(hotels).id, 
                rating=random.randint(1, 5), 
                commentary=fake.text(), 
                date_add=fake.date_this_year(), 
                moderated=random.choice([True, False]) 
            ) 
            reviews.append(review) 
        session.add_all(reviews) 
        session.commit() 
 
        bookings = [] 
        for _ in range(1000): 
            booking = Booking(

                client_id=random.choice(clients).id, 
                room_id=random.choice(rooms).id, 
                status=random.choice(list(BookingStatus)).value, 
                date_start=fake.date_this_year(), 
                date_end=fake.date_this_year(), 
                total_sum=random.uniform(100, 1000) 
            ) 
            bookings.append(booking) 
        session.add_all(bookings) 
        session.commit() 
 
if __name__ == "__main__": 
    generate_data()
