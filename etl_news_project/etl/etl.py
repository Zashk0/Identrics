import json
from sqlalchemy.orm import Session
from models import Article, engine
from etl.transform_data import transform_data  # Corrected import

session = Session(bind=engine)

def load_data(data):
    for item in data:
        if not session.query(Article).filter_by(url=item['url']).first():
            article = Article(
                title=item['title'],
                body=item['body'],
                url=item['url'],
                pub_datetime=item['pub_datetime'],
                author=item['author'],
                images=json.dumps(item['images']),
                ner=json.dumps(item['ner']),
                comments=item.get('comments', 0)
            )
            session.add(article)
    session.commit()

def etl_process():
    # Load raw data from JSON files
    with open('raw_data_restofworld.json') as f:
        raw_data_restofworld = json.load(f)
    with open('raw_data_capitalbrief.json') as f:
        raw_data_capitalbrief = json.load(f)

    raw_data = raw_data_restofworld + raw_data_capitalbrief
    transformed_data = transform_data(raw_data)
    load_data(transformed_data)

if __name__ == "__main__":
    etl_process()
