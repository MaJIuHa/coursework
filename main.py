from typing import List
from db.core import PGSession
from db.models import Hotel
from sqlalchemy import select


def add_user():
    with PGSession() as session:
        # Example of adding a user to the database
        new_hotel = Hotel(title='gg', coordinates=[34.55, 55.66], rating=0, description="Старина съебика нахуй", contacts='1488')
        session.add(new_hotel)
        session.commit()
        print("Hotel added successfully!")
        
        return new_hotel.title

def get_hotel():
    with PGSession() as session:
        # Example of adding a user to the database
        stmt = select(Hotel).where(Hotel.title == 'gg')
        res:List[Hotel] = session.execute(stmt).scalars().all()
        for i in res:
            print(i.title)


def update_hotel():
    with PGSession() as session:
        # Example of adding a user to the database
        stmt = select(Hotel).where(Hotel.title == 'gg')
        res:List[Hotel] = session.execute(stmt).scalars().all()
        for i in res:
            i.title = 'ggg+'
            session.add(i)
        session.commit()

if __name__ == '__main__':
    update_hotel()