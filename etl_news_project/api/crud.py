from sqlalchemy.orm import Session
from . import models, schemas

def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_articles(db: Session, skip: int = 0, limit: int = 5):
    articles = db.query(models.Article).offset(skip).limit(limit).all()
    return [article.to_dict() for article in articles]

def get_recent_articles(db: Session):
    articles = db.query(models.Article).order_by(models.Article.pub_datetime.desc()).limit(5).all()
    return [article.to_dict() for article in articles]

def get_last_inserted_article(db: Session):
    article = db.query(models.Article).order_by(models.Article.id.desc()).first()
    return article.to_dict() if article else None

def search_articles(db: Session, query: str):
    articles = db.query(models.Article).filter(models.Article.title.contains(query)).all()
    return [article.to_dict() for article in articles]

def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(
        title=article.title,
        url=article.url,
        body=article.body,
        pub_datetime=article.pub_datetime,
        author=article.author,
        images=article.images,
        ner=article.ner
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article.to_dict()

def update_article(db: Session, article_id: int, article: schemas.ArticleUpdate):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if db_article is None:
        return None
    for key, value in article.dict().items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article.to_dict()

def delete_article(db: Session, article_id: int):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if db_article is None:
        return None
    db.delete(db_article)
    db.commit()
    return db_article.to_dict()

def get_articles_by_date(db: Session, pub_date: str):
    articles = db.query(models.Article).filter(models.Article.pub_datetime == pub_date).all()
    return [article.to_dict() for article in articles]

def get_articles_by_author(db: Session, author: str):
    articles = db.query(models.Article).filter(models.Article.author == author).all()
    return [article.to_dict() for article in articles]
