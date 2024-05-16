from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    body = Column(Text)
    url = Column(String, unique=True)
    pub_datetime = Column(DateTime)
    author = Column(String)
    images = Column(Text)
    ner = Column(Text)
    comments = Column(Integer)

engine = create_engine('sqlite:///articles.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
