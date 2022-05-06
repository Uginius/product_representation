from pprint import pprint

with open('src/oz', 'r', encoding='utf8') as file:
    rqs = {}
    cat_id_str = None
    categories = {}
    cat_id = 0
    req_id = 0
    for line in file:
        txt = line.strip()
        if line[0].strip():
            cat_id += 1
            cat_id_str = f'OZ{cat_id:03}'
            rqs[cat_id_str] = {}
            categories[cat_id_str] = txt
        else:
            req_id += 1
            rqs[cat_id_str][f'oz_{req_id:04}'] = txt
    pprint(categories)
    pprint(rqs)
