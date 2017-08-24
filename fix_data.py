#!/usr/bin/env python3

"""Fix an IOB-tagged data file, remove Quantity and Unit tags before an 
Ingredient tag, and expand the Ingredient tags to include the preceding 
determiner"""

class IOBLine:
    def __init__(self, line):
        self.cells = line.split('\t')
        self.is_empty_line = True
        if len(self.cells) > 1:
            self.is_empty_line = False
            self.ent_id = self.cells[0]
            self.start = self.cells[1]
            self.end = self.cells[2]
            self.text = self.cells[3]
            self.stemmed_text = self.cells[4]
            self.pos = self.cells[6]

    def set_ent_id(self, new_id):
        self.cells[0] = new_id
        self.ent_id = new_id

    def to_string(self):
        return '\t'.join(self.cells)

def remove_quantity_unit(line_index, lines):
    line = lines[line_index]
    if not (line.ent_id.startswith('Q') or line.ent_id.startswith('U')):
        raise Exception("The token to be fixed must be in a Quantity or Unit "+ 
                        "tag")
    next_ing_index = find_next_ingredient_index(line_index, lines)
    ing_id = lines[next_ing_index].ent_id
    for i in range(line_index, next_ing_index):
        if not lines[i].is_empty_line:
            lines[i].set_ent_id(ing_id)

def include_determiner(line_index, lines):
    this_line = lines[line_index]
    prev_index = line_index - 1
    while prev_index > 0 and not lines[prev_index].is_empty_line and \
                                             lines[prev_index].pos == "DET":
        lines[prev_index].set_ent_id(this_line.ent_id)
        prev_index -= 1


def find_next_ingredient_index(line_index, lines):
    while line_index < len(lines):
        l = lines[line_index]
        if not l.is_empty_line and (l.ent_id.startswith('I') or 
                                    l.ent_id.startswith('T')):
            return line_index
        line_index += 1
    return line_index - 1

if __name__ == "__main__":
    import sys, os
    from utils import file_ops

    input_dir = sys.argv[1]

    file_paths = file_ops.find_files_in_dir(input_dir, extension=".entity")

    for f in file_paths:
        with open(f, 'r') as input_doc:
            lines = [IOBLine(l.strip()) for l in input_doc]
            for i in range(len(lines)):
                line = lines[i]
                if not line.is_empty_line and (line.ent_id.startswith('Q') or 
                                               line.ent_id.startswith('U')):
                    remove_quantity_unit(i, lines)

            for i in range(len(lines)):
                line = lines[i]
                if not line.is_empty_line and (line.ent_id.startswith('I') or 
                                               line.ent_id.startswith('T')):
                    include_determiner(i, lines)

            output_doc = open(f, 'w')
            for l in lines:
                output_doc.write(l.to_string()+'\n')
            output_doc.close()
