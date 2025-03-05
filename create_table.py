from db.core import engine
from db.base import Base

def main():
    
    Base.metadata.create_all(bind=engine)
        

if __name__ == '__main__':
    main()