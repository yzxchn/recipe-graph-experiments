#!/usr/bin/env python3

class Entity:
    """A class that represents an entity in a converted .entity document.
    """
    def __init__(self, cells):
        """
        Arguments:
        cells: a list of items in one line in the .entity document
        """
        self.id = cells[0]
        self.beg = int(cells[1])
        self.end = int(cells[2])
        self.text = cells[3]
        self.tokens = [self.text]
        self.pos = [cells[4]]

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
        self.pos.append(cells[4])

