import os

from databases import Database
from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

db_url = os.environ['DB_URL']

database = Database(db_url)
metadata_obj = MetaData()

engine = create_engine(db_url)

Base = declarative_base(metadata=metadata_obj)
