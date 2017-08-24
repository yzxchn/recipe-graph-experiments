import csv, pickle

ing_name_set = set()

with open('ingr_info.tsv') as ingr_info:
    tsv = csv.reader(ingr_info, delimiter='\t')
    for row in tsv:
        name = row[1]
        for t in name.split('_'):
            ing_name_set.add(t)

with open('ingr_name_set', 'wb') as ingr_name_set:
    pickle.dump(ing_name_set, ingr_name_set)
