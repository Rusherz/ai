import sqlalchemy as db

from models.Annotation import Annotation

# From SQL Alchemy, import useful functions and classes that
# are for use within the configuration and instantiation of our database.
from sqlalchemy.orm import sessionmaker

# Our engine will act as our connector. This needs to persist for the duration of our
# script, whether exected with a completion, or left running indefinitely.
Engine = db.create_engine(
    'mysql+pymysql://server:^C{WZwVa4&kvxhd\'@jmir-mysql-production.cmlc7celvj8o.us-east-2.rds.amazonaws.com:3306/jmir-ml?charset=utf8')

# A factory for our connection is made available for us through the session maker.
Session = sessionmaker(bind=Engine)

# Creating an instance of our session via our factory.
session = Session()

annotations = session.query(Annotation).limit(1000).all()

TRAIN_DATA = []

for annotation in annotations:
    TRAIN_DATA.append((
        annotation.document, {
            'entities': [
                (
                    annotation.start,
                    annotation.end,
                    annotation.entity
                )
            ]
        }
    ))
