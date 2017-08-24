def find_act_act_pairs(recipe_obj):
    flow_links = recipe_obj.get_flow_links()
    pairs = []
    for id1, id2 in flow_links:
        if id1.startswith('A') and id2.startswith('A'):
            pairs.append(((recipe_obj.ins_entities.get_entity(id1), 
                          recipe_obj.ins_entities.get_entity(id2)), recipe_obj))
    return pairs
