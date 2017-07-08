#!/usr/bin/env python3
import crfutils

separator = '\t'

fields = 'y w pos'

templates = []

templates += [(('w', i),) for i in range(-2, 3)]
templates += [(('w', i),('w', i+1)) for i in range(-2, 2)]
templates += [(('pos', i),) for i in range(-2, 2)]
templates += [(('pos', i),('pos', i+1)) for i in range(-2, 2)]

def feature_extractor(X):
    crfutils.apply_templates(X, templates)
    if X:
        X[0]['F'].append('__BOS__')
        X[-1]['F'].append('__EOS__')

if __name__ == '__main__':
    crfutils.main(feature_extractor, fields=fields, sep=separator)

