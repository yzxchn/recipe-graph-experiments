#!/usr/bin/env python3
from .entity_reader import RecipeEntityReader
from .attribute_reader import AttributeReader
from collections import defaultdict

"""An interface for the preprocessed recipe data."""

class PreprocessedRecipe:
    def __init__(self, ing_fp, ins_fp, link_fp, atts_fp):
        """
        ing_fp: an ingredient file object
        ins_fp: an instruction file object
        link_fp: a link file object
        """
        self._load_atts(atts_fp)
        self._load_ing(ing_fp)
        self._load_ins(ins_fp)
        self._load_link(link_fp)

    def _load_atts(self, atts_fp):
        self.atts = AttributeReader(atts_fp)

    def _load_ing(self, ing_fp):
        self.ing_entities = RecipeEntityReader(ing_fp, self.atts)
        ing_fp.seek(0)
        self.ing_num_lines = 0
        self.ing_lines = []
        current_line = []
        for l in ing_fp:
            if l == '\n':
                self.ing_num_lines += 1
                self.ing_lines.append(current_line)
                current_line = []
            else:
                current_line.append(l.split('\t')[3])

    def _load_ins(self, ins_fp):
        self.ins_entities = RecipeEntityReader(ins_fp, self.atts)
        ins_fp.seek(0)
        self.ins_num_lines = 0
        self.ins_lines = []
        current_line = []
        for l in ins_fp:
            if l == '\n':
                self.ins_num_lines += 1
                self.ins_lines.append(current_line)
                current_line = []
            else:
                current_line.append(l.split('\t')[3])

    def _load_link(self, link_fp):
        self.coref_links = []
        self.coref_links_set = set()
        self.flow_links = []
        self.flow_links_set = set()
        for l in link_fp:
            cells = l.strip().split('\t')
            if len(cells) < 5:
                continue
            else:
                lid = cells[0]
                l = (cells[1], cells[3])
                if lid.startswith('F'):
                    self.flow_links.append(l)
                    self.flow_links_set.add(l)
                elif lid.startswith('C'):
                    self.coref_links.append(l)
                    self.coref_links_set.add(l)
        self._load_link_map()

    def _load_link_map(self):
        self.flow_connect_to = defaultdict(set)
        self.flow_connected_by = defaultdict(set)
        self.coref_connect_to = defaultdict(set)
        self.coref_connected_by = defaultdict(set)

        for fl, fr in self.flow_links:
            self.flow_connect_to[fl].add(fr)
            self.flow_connected_by[fr].add(fl)
        for cl, cr in self.coref_links:
            self.coref_connect_to[cl].add(cr)
            self.coref_connected_by[cr].add(cl)
        
    def get_ing_entities(self):
        return self.ing_entities.get_entities()

    def get_ins_entities(self):
        return self.ins_entities.get_entities()

    def get_coref_links(self):
        return self.coref_links

    def get_flow_links(self):
        return self.flow_links

    def are_related(self, entity1, entity2):
        """Returns True if the two entities have a relation link in the recipe 
        (order matters), otherwise false."""
        pair = (entity1.id, entity2.id)
        return pair in self.coref_links_set or pair in self.flow_links_set

    def get_connected_flow_entities(self, id_):
        connected_ids = self.flow_connect_to[id_]
        entities = []
        for d in connected_ids:
            entities.append(self.ins_entities.get_entity(d))
        return entities

    def get_connecting_flow_entities(self, id_):
        connecting_ids = self.flow_connected_by[id_]
        entities =[]
        for d in connecting_ids:
            entities.append(self.ins_entities.get_entity(d))
        return entities
