#!/usr/bin/env python3
from .entity_classes import *
class RecipeEntityReader:
    def __init__(self, fp, atts):
        self.entity_file = fp
        self.atts = atts
        self._load_entities()

    def _load_entities(self):
        self.entities = {}
        self.ordered_entities = []
        sent_i = 0
        tok_i = 0
        for line in self.entity_file:
            cells = line.split()
            if len(cells) > 1:
                self._add_entity(cells, sent_i, tok_i)
                tok_i += 1
            else:
                sent_i += 1
                tok_i = 0
        
    def _add_entity(self, cells, sent_i, tok_i):
        """Cells: a list of items in one line in the entity document
        """
        id_ = cells[0]
        if not id_ == '-':
            if id_ in self.entities:
                self.entities[id_].extend(cells)
            else:
                if id_.startswith('I'):
                    is_start, is_compound = self.atts.get_ing_att(id_)
                    entity = Ingredient(cells, sent_i, tok_i, 
                                        is_start, is_compound)
                elif id_.startswith('A'):
                    act_type = self.atts.get_act_att(id_)
                    entity = Action(cells, sent_i, tok_i, act_type)
                else:
                    entity = Entity(cells, sent_i, tok_i)
                self.entities[id_] = entity
                self.ordered_entities.append(entity)
    
    def get_entities(self):
        return self.ordered_entities

    def get_entity(self, id_):
        return self.entities.get(id_)
