from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "url": self.url,
            "pub_datetime": self.pub_datetime.isoformat(),
            "author": self.author,
            "images": json.loads(self.images),
            "ner": json.loads(self.ner),
            "comments": self.comments
        }

engine = create_engine('sqlite:///articles.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
