from pprint import pprint
from src.wb_terms import wb_terms
from src.oz_terms import oz_terms

req_id = 0
reqs = {}
oz = ['src/oz', 'oz']
wb = ['src/wb', 'wb']

mp = oz

if mp == oz:
    terms = oz_terms
else:
    terms = wb_terms

for el in terms:
    category_terms = terms[el]
    phrases = []
    cat_reqs = {}
    for phr in category_terms:
        term = category_terms[phr]
        if term in phrases:
            continue
        req_id += 1
        cat_reqs[f'{mp[1]}_{req_id:04}'] = term
        phrases.append(term)
    reqs[el] = cat_reqs
pprint(reqs)
