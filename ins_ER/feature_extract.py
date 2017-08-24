#!/usr/bin/env python3
import crfutils

separator = '\t'

fields = 'y w lem pos1 pos2 dep pw plem ppos1 ppos2 pdep ppw pplem pppos1 '+\
         'pppos2 ppdep'

templates = []

templates += [(('w', i),) for i in range(-2, 3)]
templates += [(('w', i),('w', i+1)) for i in range(-2, 2)]

templates += [(('lem', i),) for i in range(-2, 3)]
templates += [(('lem', i),('lem', i+1)) for i in range(-2, 2)]

templates += [(('pos1', i),) for i in range(-2, 2)]
templates += [(('pos1', i),('pos1', i+1)) for i in range(-2, 2)]
templates += [(('pos2', i),) for i in range(-2, 2)]
templates += [(('pos2', i),('pos2', i+1)) for i in range(-2, 2)]

templates += [(('pw', i),) for i in range(-2, 3)]
templates += [(('w', i), ('pw', i)) for i in range(-2, 3)]
templates += [(('pw', i), ('ppw', i)) for i in range(-2, 3)]
templates += [(('w', i), ('pw', i), ('ppw', i)) for i in range(-2, 3)]

templates += [(('ppos1', i),) for i in range(-2, 3)]
templates += [(('pos1', i), ('ppos1', i)) for i in range(-2, 3)]
templates += [(('ppos1', i), ('pppos1', i)) for i in range(-2, 3)]
templates += [(('pos1', i), ('ppos1', i), ('pppos1', i)) for i in range(-2, 3)]

templates += [(('ppos2', i),) for i in range(-2, 3)]
templates += [(('pos2', i), ('ppos2', i)) for i in range(-2, 3)]
templates += [(('ppos2', i), ('pppos2', i)) for i in range(-2, 3)]
templates += [(('pos2', i), ('ppos2', i), ('pppos2', i)) for i in range(-2, 3)]

templates += [(('pos1', i), ('dep', i), ('ppos1', i)) for i in range(-2, 3)]
templates += [(('pos1', i), ('dep', i), ('ppos1', i), 
                            ('pdep', i), ('pppos1', i)) for i in range(-2, 3)]
templates += [(('pos2', i), ('dep', i), ('ppos2', i)) for i in range(-2, 3)]
templates += [(('pos2', i), ('dep', i), ('ppos2', i), 
                            ('pdep', i), ('pppos2', i)) for i in range(-2, 3)]

templates += [(('in_ingr_set', i),) for i in range(-2, 3)]
templates += [(('in_ingr_set', i), ('in_ingr_set', i+1)) for i in range(-2, 2)]
templates += [(('is_capitalized', i),) for i in range(-2, 3)]
templates += [(('is_capitalized', i), ('is_capitalized', i+1)) for i in range(-2, 2)]


def is_capitalized(token):
    """Check if the token's first character is captalized, and the rest lower 
    case. (If the token is title case)
    """
    return token.istitle()

def is_in_ingr_name_set(token):
    import pickle
    name_set = pickle.load(open('./ing_names/ingr_name_set', 'rb'))
    return token in name_set

def b(v):
    return 'yes' if v else 'no'

def observation(v):
    v['in_ingr_set'] = b(is_in_ingr_name_set(v['w'].lower()))
    v['is_capitalized'] = b(is_capitalized(v['w']))

def feature_extractor(X):
    for x in X:
        observation(x)
    crfutils.apply_templates(X, templates)
    if X:
        X[0]['F'].append('__BOS__')
        X[-1]['F'].append('__EOS__')

if __name__ == '__main__':
    crfutils.main(feature_extractor, fields=fields, sep=separator)
