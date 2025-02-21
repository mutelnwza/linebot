import json

def formatjson(data):
    with open('userinput.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)