import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

db_path = os.path.join(os.path.dirname(__file__), 'phalanx.db')

engine = create_engine(f'sqlite:///{db_path}')

def create_tables() -> None:
    Base.metadata.create_all(engine)
    
    return None

# Create a session factory
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a globally accessible scoped session
Session = scoped_session(SessionFactory)