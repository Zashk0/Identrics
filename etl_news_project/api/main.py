from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from .insert_json_to_db import insert_json_to_db
from typing import List

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/articles/", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles

@app.get("/articles/recent", response_model=List[schemas.Article])
def read_recent_articles(db: Session = Depends(get_db)):
    articles = crud.get_recent_articles(db)
    return articles

@app.get("/articles/last", response_model=schemas.Article)
def read_last_inserted_article(db: Session = Depends(get_db)):
    article = crud.get_last_inserted_article(db)
    return article

@app.get("/articles/search", response_model=List[schemas.Article])
def search_articles(query: str, db: Session = Depends(get_db)):
    articles = crud.search_articles(db, query=query)
    return articles

@app.get("/articles/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.post("/articles/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.create_article(db, article=article)

@app.put("/articles/{article_id}", response_model=schemas.Article)
def update_article(article_id: int, article: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    db_article = crud.update_article(db, article_id=article_id, article=article)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.delete("/articles/{article_id}", response_model=schemas.Article)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = crud.delete_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.get("/articles/date/{pub_date}", response_model=List[schemas.Article])
def read_articles_by_date(pub_date: str, db: Session = Depends(get_db)):
    articles = crud.get_articles_by_date(db, pub_date=pub_date)
    return articles

@app.get("/articles/author/{author}", response_model=List[schemas.Article])
def read_articles_by_author(author: str, db: Session = Depends(get_db)):
    articles = crud.get_articles_by_author(db, author=author)
    return articles

if __name__ == "__main__":
    import uvicorn
    db = next(get_db())
    insert_json_to_db('etl_news_project/spiders/raw_data_capitalbrief.json', db)
    insert_json_to_db('etl_news_project/spiders/raw_data_rest_of_world.json', db)
    uvicorn.run(app, host="0.0.0.0", port=8000)
