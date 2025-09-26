import json

with open('ink_bufan.json', encoding='utf-8') as f:
    data = json.load(f)

for name, src in data:
    # create a directory for each name
    import os

    os.makedirs(name, exist_ok=True)
    for k, v in src.items():
        if not k:
            continue
        path = f'{name}/{k}'
        print(path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(v)