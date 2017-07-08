#!/usr/bin/env python3
from .entity_classes import *
class RecipeEntityReader:
    def __init__(self, entity_file_path):
        with open(entity_file_path) as self.ent_doc:
            self._load_entities()

    def _load_entities(self):
        self.entities = {}
        for line in self.ent_doc:
            cells = line.split()
            if len(cells) > 1:
                self._add_entity(cells)
        
    def _add_entity(self, cells):
        """Cells: a list of items in one line in the entity document
        """
        id_ = cells[0]
        if not id_ == '-':
            if id_ in self.entities:
                self.entities[id_].extend(cells)
            else:
                entity = Entity(cells)
                self.entities[id_] = entity
    
    def get_entities(self):
        return self.entities.values()
