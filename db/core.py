import os
from typing import Generator
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
PGSession: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_session() -> Generator:
    async with PGSession() as session:
        yield session