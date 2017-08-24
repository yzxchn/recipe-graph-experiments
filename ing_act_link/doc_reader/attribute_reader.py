#!/usr/bin/env python

"""Serves as an interface to an .atts file in the data directory.
"""

class AttributeReader:
    def __init__(self, fp):
        self.atts_file = fp
        self._load_atts()

    def _load_atts(self):
        self.act_atts = {}
        self.ing_atts = {}
        for l in self.atts_file:
            cells = l.strip().split('\t')
            if len(cells) < 2:
                continue
            else:
                if cells[0].startswith('I'):
                    self.ing_atts[cells[0]] = (cells[1], cells[2])
                elif cells[0].startswith('A'):
                    self.act_atts[cells[0]] = cells[1]

    def get_act_att(self, act_id):
        return self.act_atts[act_id]

    def get_ing_att(self, ing_id):
        return self.ing_atts[ing_id]
