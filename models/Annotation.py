from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Our declarative base comes from SQL Alchemy and will be the basis to most of our
# models. This allows us to immediately inherit properties necessary for querying.
Base = declarative_base()


class Annotation(Base):
    __tablename__ = 'annotations'

    id = Column('id', Integer, primary_key=True)
    document = Column('document', String)
    annotation = Column('annotation', String)
    start = Column('start', Integer)
    end = Column('end', Integer)
    entity = Column('entity', String)

    def __repr__(self):
        return "<Annotation(annotation='%s')>" % (self.annotation)
