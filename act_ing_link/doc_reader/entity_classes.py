#!/usr/bin/env python3

class Entity:
    """A class that represents an entity in a converted .entity document.
    """
    def __init__(self, cells, sent_i, tok_i):
        """
        Arguments:
        cells: a list of items in one line in the .entity document
        sent_i: the sentence index this entity is in
        tok_i: the index of this token within the sentence
        """
        self.id = cells[0]
        self.beg = int(cells[1])
        self.end = int(cells[2])
        self.text = cells[3]
        self.tokens = [self.text]
        self.lemmas = [cells[4]]
        self.pos = [cells[5]]
        self.pos_simple = [cells[6]]
        self.sent_i = sent_i
        self.tok_i = tok_i

    def extend(self, cells):
        """Since an entity can span multiple tokens, use this method to 
        extend this entity.
        """
        # extend the text, add space if the beginning index of the new token
        # does not follow the old ending index
        self.text = (' '*(int(cells[1]) - self.end)).join([self.text, cells[3]]) 
        #extend the beginning and ending indexes:
        self.end = int(cells[2])
        self.tokens.append(cells[3])
        self.lemmas.append(cells[4])
        self.pos.append(cells[5])
        self.pos_simple.append(cells[6])

class Action(Entity):
    def __init__(self, cells, sent_i, tok_i, act_type):
        super(Action, self).__init__(cells, sent_i, tok_i)
        self.act_type = act_type

class Ingredient(Entity):
    def __init__(self, cells, sent_i, tok_i, is_start, is_compound):
        super(Ingredient, self).__init__(cells, sent_i, tok_i)
        self.is_start = is_start
        self.is_compound = is_compound
