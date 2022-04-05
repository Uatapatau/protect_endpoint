from sqlalchemy import Column, Text, create_engine, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()

def create_db():
    engine = create_engine('sqlite:///sqlite.db')
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
    return engine


class ChekSum(Base):

    __tablename__ = 'ChekSum'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False,
                unique=True)
    author_name = Column(Text)
    file_check_sum = Column(Text)

    def __init__(self, file_check_sum, author_name):
        self.author_name = author_name
        self.file_check_sum = file_check_sum

def create_row(engine, table, kwargs):
    with Session(engine) as session:
        row = session.query(table).filter_by(**kwargs).first()
        if row is None:
            session.add(table(**kwargs))
            session.commit()
        else:
            raise Exception