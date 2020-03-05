import json

def dict_to_json(dict):
    return json.dumps(dict, ensure_ascii=False).encode('utf-8')

def json_to_dict(json_text):
    return json.loads(json_text)

def json_to_book(json_text):
    json_dict = json.loads(json_text)
    return json_dict

with open('../cleaned_pickles/ivan_ilyich_book.json', 'r') as f:
    raw_text = f.read()
book = json_to_book(raw_text)
x = 5