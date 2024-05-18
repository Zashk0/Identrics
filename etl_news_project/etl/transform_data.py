import re
import spacy
from jsonschema import validate, ValidationError
import html
import unicodedata

# Load the small English model for spaCy
nlp = spacy.load("en_core_web_sm")

# JSON Schema for data validation
article_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "body": {"type": "string"},
        "url": {"type": "string"},
        "pub_datetime": {"type": "string", "format": "date-time"},
        "author": {"type": "string"},
        "images": {
            "type": "array",
            "items": {"type": "string"}
        },
        "ner": {"type": "object"},
        "comments": {"type": "integer"}
    },
    "required": ["title", "body", "url", "pub_datetime", "author", "images", "ner"]
}

def clean_html(raw_html):
    # Remove HTML tags
    clean_re = re.compile('<.*?>')
    clean_text = re.sub(clean_re, '', raw_html)
    # Decode HTML entities
    clean_text = html.unescape(clean_text)
    # Decode Unicode escape sequences
    clean_text = clean_text.encode('utf-8').decode('unicode_escape')
    # Normalize Unicode characters
    clean_text = unicodedata.normalize('NFKD', clean_text)
    return clean_text

def extract_entities(text):
    doc = nlp(text)
    entities = {"Person": [], "Organization": [], "Location": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities

def validate_article(article):
    try:
        validate(instance=article, schema=article_schema)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False

def transform_data(raw_data):
    transformed_data = []
    for item in raw_data:
        item['body'] = clean_html(item['body'])
        item['ner'] = extract_entities(item['body'])
        if validate_article(item):
            transformed_data.append(item)
    return transformed_data
