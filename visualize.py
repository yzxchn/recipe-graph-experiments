#!/usr/bin/env python3

import graphviz as gv
from doc_reader.doc_reader import *
import sys

entity_path, link_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]

entities = RecipeEntityReader(entity_path).get_entities()
graph = gv.Digraph(format='svg')
for entity in entities:
    graph.node(entity.id, entity.text)
with open(link_path) as link_doc:
    for line in link_doc:
        cells = line.strip().split('\t')
        if len(cells) == 5 and cells[0].startswith('F'):
            graph.edge(cells[1], cells[3])

graph.render(output_path)
