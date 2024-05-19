from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    body = Column(Text, nullable=True)
    pub_datetime = Column(DateTime)
    author = Column(String, index=True)
    images = Column(Text, nullable=True)
    ner = Column(Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "body": self.body,
            "pub_datetime": self.pub_datetime,
            "author": self.author,
            "images": json.loads(self.images) if self.images else [],  # Deserialize the JSON string back to a list
            "ner": json.loads(self.ner) if self.ner else {}  # Deserialize the JSON string back to a dict
        }
