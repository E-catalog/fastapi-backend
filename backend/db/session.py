import os

from databases import Database
from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()

db_url = os.environ['DB_URL']

database = Database(db_url)
metadata_obj = MetaData()

engine = create_engine(db_url)
#db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base(metadata=metadata_obj)
#Base.query = db_session.query_property()
