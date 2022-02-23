from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text

from backend.db.session import metadata_obj

Places = Table(
    'places',
    metadata_obj,
    Column('uid', Integer, primary_key=True),
    Column('name', String, unique=True, nullable=False),
    Column('head_of_excavations', String),
    Column('type_of_burial_site', String),
    Column('coordinates', String),
    Column('comments', Text),
)

Individuals = Table(
    'individuals',
    metadata_obj,
    Column('uid', Integer, primary_key=True),
    Column('place_uid', Integer, ForeignKey('places.uid', ondelete='CASCADE'), nullable=False),
    Column('name', String, nullable=False),
    Column('year_of_excavation', Integer),
    Column('individual_type', String),
    Column('sex', String),
    Column('age', String),
    Column('preservation', String),
    Column('epoch', String),
    Column('comments', Text),
)
