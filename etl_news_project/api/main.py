from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel  # Import BaseModel from pydantic

from database import SessionLocal, engine, get_db
from models import Article, Base

app = FastAPI()

class ArticleSchema(BaseModel):
    title: str
    body: str
    url: str
    pub_datetime: datetime
    author: str
    images: List[str]
    ner: dict
    comments: int

# Create the database tables
Base.metadata.create_all(bind=engine)

@app.get("/articles/", response_model=List[ArticleSchema])
def get_articles(page: int = 0, db: Session = Depends(get_db)):
    articles = db.query(Article).offset(page * 5).limit(5).all()
    return [article.to_dict() for article in articles]

@app.get("/articles/date/", response_model=List[ArticleSchema])
def get_articles_by_date(date: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(func.date(Article.pub_datetime) == date).all()
    return [article.to_dict() for article in articles]

@app.get("/articles/author/", response_model=List[ArticleSchema])
def get_articles_by_author(author: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.author == author).all()
    return [article.to_dict() for article in articles]

@app.get("/article/{article_id}", response_model=ArticleSchema)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article.to_dict()

@app.post("/article/", response_model=ArticleSchema)
def create_article(article: ArticleSchema, db: Session = Depends(get_db)):
    db_article = Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article.to_dict()

@app.delete("/article/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return {"message": "Article deleted"}

@app.put("/article/{article_id}", response_model=ArticleSchema)
def update_article(article_id: int, article: ArticleSchema, db: Session = Depends(get_db)):
    db_article = db.query(Article).get(article_id)
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in article.dict().items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article.to_dict()

@app.get("/articles/recent", response_model=List[ArticleSchema])
def get_recent_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.pub_datetime.desc()).limit(5).all()
    return [article.to_dict() for article in articles]

@app.get("/articles/last", response_model=ArticleSchema)
def get_last_article(db: Session = Depends(get_db)):
    article = db.query(Article).order_by(Article.id.desc()).first()
    if not article:
        raise HTTPException(status_code=404, detail="No articles found")
    return article.to_dict()

@app.get("/articles/search/", response_model=List[ArticleSchema])
def search_articles(query: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(
        Article.title.contains(query) | Article.body.contains(query)
    ).all()
    return [article.to_dict() for article in articles]

@app.get("/articles/popular", response_model=List[ArticleSchema])
def get_popular_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).order_by(Article.comments.desc()).limit(5).all()
    return [article.to_dict() for article in articles]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
