from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, Text

from backend.db.session import metadata_obj

#from sqlalchemy.orm import relationship

#from backend.db.session import Base

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

"""
class Places(Base):
    __tablename__ = 'places'

    uid = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    head_of_excavations = Column(String)
    type_of_burial_site = Column(String)
    coordinates = Column(String)
    comments = Column(Text)
    individuals = relationship('Individuals', lazy='joined', back_populates='place')

    def __repr__(self):
        return f'Место: индекс в базе {self.id}, {self.place}'


class Individuals(Base):
    __tablename__ = 'individuals'

    uid = Column(Integer, primary_key=True)
    place_uid = Column(Integer, ForeignKey(Places.uid, ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    year_of_excavation = Column(Integer)
    individual_type = Column(String)
    sex = Column(String)
    age = Column(String)
    preservation = Column(String)
    epoch = Column(String)
    comments = Column(Text)
    place = relationship('Places', lazy='joined', back_populates='individuals')

    def __repr__(self):
        return 'Индвид: индекс [{uid}], {place}, {name}, {sex}, {age}'.format(
            uid=self.id,
            place=self.place,
            name=self.name,
            sex=self.sex,
            age=self.age,
        )
"""
