
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# we have to specify where is our database located with this format 'postgressql://<username>:<password>@<ip_address/hostname>/databasename>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:wang@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)

Base = declarative_base()

# this function is a dependency that creates a session each time w use the database then closes it when we are done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()