from utils.file_ops import *

files = find_files_in_dir('../data/ing_entity', '.ient')

total = 0
o_count = 0

for f in files:
    ing_file = open(f)
    for l in ing_file:
        if len(l) < 4:
            continue
        elif l.startswith('-'):
            o_count += 1
            total += 1
        else:
            total += 1

print(o_count/total)
