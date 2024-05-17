import sys
print(sys.path)  # Add this to see the current PYTHONPATH

from sqlalchemy.orm import sessionmaker
from models import Article, engine  # Adjusted import path to include project root
from etl.transform_data import clean_html, extract_entities  # Adjust the import path
import json

class NewsSpidersPipeline:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        article = session.query(Article).filter_by(url=item['url']).first()
        
        if article:
            session.close()
            return item
        
        article = Article(
            title=item['title'],
            body=clean_html(item['body']),
            url=item['url'],
            pub_datetime=item['pub_datetime'],
            author=item['author'],
            images=json.dumps(item['images']),
            ner=json.dumps(extract_entities(clean_html(item['body']))),
            comments=item.get('comments', 0)
        )
        
        try:
            session.add(article)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
