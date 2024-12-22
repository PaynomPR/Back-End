import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

# "postgresql+psycopg2://postgres:nblIF4Wop2eGfYYJ@db.ltyhskwmttkrernknvvr.supabase.co:5432/postgres"

driver_name = os.environ.get("DB_DRVR")
user_name = os.environ.get("DB_USER")
password = os.environ.get("DB_PASS")
host = os.environ.get("DB_HOST")
database = os.environ.get("DB_NAME")
port = os.environ.get("DB_PORT")

DATABASE_URL = URL.create(
    drivername=driver_name,
    username=user_name,
    password=password,
    host=host,
    database=database,
    port=port,
)


engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()


class Base(DeclarativeBase):
    pass


def init_db():
    Base.metadata.create_all(bind=engine)
