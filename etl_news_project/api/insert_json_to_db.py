import json
from sqlalchemy.orm import Session
from datetime import datetime
from . import models

def insert_json_to_db(json_file: str, db: Session):
    with open(json_file, 'r', encoding='utf-8') as file:
        articles_data = json.load(file)

        for article_data in articles_data:
            pub_datetime_str = article_data.get('pub_datetime', '2024-01-01T00:00:00')
            
            # Adjust the string to match the required format
            pub_datetime_str = pub_datetime_str.replace('T', ' ')
            if len(pub_datetime_str) == 10:  # if date only
                pub_datetime_str += ' 00:00:00'
            
            pub_datetime = datetime.strptime(pub_datetime_str, '%Y-%m-%d %H:%M:%S')

            article = models.Article(
                title=article_data['title'],
                url=article_data['url'],
                body=article_data.get('body', ""),
                pub_datetime=pub_datetime,
                author=article_data['author'],
                images=json.dumps(article_data['images']),
                ner=json.dumps(article_data['ner'])
            )
            db.add(article)
        db.commit()

if __name__ == "__main__":
    from .database import SessionLocal
    db = SessionLocal()
    insert_json_to_db('etl_news_project/spiders/raw_data_capitalbrief.json', db)
    insert_json_to_db('etl_news_project/spiders/raw_data_rest_of_world.json', db)
