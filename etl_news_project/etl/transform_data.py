import re
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_html(raw_html):
    clean_re = re.compile('<.*?>')
    clean_text = re.sub(clean_re, '', raw_html)
    return clean_text

def extract_entities(text):
    doc = nlp(text)
    entities = {"Person": [], "Organization": [], "Location": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities

def transform_data(raw_data):
    transformed_data = []
    for item in raw_data:
        item['body'] = clean_html(item['body'])
        item['ner'] = extract_entities(item['body'])
        transformed_data.append(item)
    return transformed_data
