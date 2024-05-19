from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class ArticleBase(BaseModel):
    title: str
    url: str
    body: Optional[str] = None
    pub_datetime: datetime
    author: str
    images: List[str]
    ner: Dict[str, List[str]]

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int

    class Config:
        orm_mode = True
