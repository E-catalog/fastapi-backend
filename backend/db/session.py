import os

import databases
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()

db_url = os.environ['DB_URL']

database = databases.Database(db_url)

engine = create_engine(db_url)
#db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
#Base.query = db_session.query_property()
