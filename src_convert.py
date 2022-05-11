from pprint import pprint
oz = ['src/oz', 'oz']
wb = ['src/wb', 'wb']

mp = wb
with open(mp[0], 'r', encoding='utf8') as file:
    rqs = {}
    cat_id_str = None
    categories = {}
    cat_id = 0
    req_id = 0
    for line in file:
        txt = line.strip()
        if line[0].strip():
            cat_id += 1
            cat_id_str = f'{mp[1].upper()}{cat_id:03}'
            rqs[cat_id_str] = {}
            categories[cat_id_str] = txt
        else:
            req_id += 1
            rqs[cat_id_str][f'{mp[1]}_{req_id:04}'] = txt
    pprint(categories)
    pprint(rqs)
