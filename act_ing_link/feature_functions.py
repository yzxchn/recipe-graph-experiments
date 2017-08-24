from doc_reader.entity_classes import *

def baseline_predictor(entity1, entity2, recipe_obj):
    """If entity1 and entity2 have exactly one other Action entity in between, 
    believe that they are connected"""
    entities = recipe_obj.get_ins_entities()
    ent1_i = -1
    ent2_i = -1
    for i in range(len(entities)):
        if entities[i] is entity1:
            ent1_i = i
        elif entities[i] is entity2:
            ent2_i = i
    assert ent1_i >=0 and ent2_i >= 0 and ent1_i < ent2_i
    act_count = 0
    for i in range(ent1_i+1, ent2_i):
        if isinstance(entities[i], Action):
            act_count += 1
    return "baseline_decision", act_count == 1

def sent_distance(ent1, ent2, recipe):
    return "sent_distance", ent2.sent_i - ent1.sent_i

def num_actions_between(ent1, ent2, recipe):
    entities = recipe.get_ins_entities()
    ent1_i = -1
    ent2_i = -1
    for i in range(len(entities)):
        if entities[i] is ent1:
            ent1_i = i
        elif entities[i] is ent2:
            ent2_i = i
    assert ent1_i >=0 and ent2_i >= 0 and ent1_i < ent2_i
    act_count = 0
    for i in range(ent1_i+1, ent2_i):
        if isinstance(entities[i], Action):
            act_count += 1
    return "num_actions_between", act_count

def action_type(ent1, ent2, recipe):
    return "action_type", ent1.act_type

def ing_text(ent1, ent2, recipe):
    return "ing_text", ent2.text

def act_type_ing_text(ent1, ent2, recipe):
    return "act_type_ing_text", ent1.act_type+"|"+ent2.text

def linked_ingredients(ent1, recipe_obj):
    """for a given action entity, find out the Ingredient entities that are 
    linked to it"""
    linked_entities = recipe_obj.get_connecting_flow_entities(ent1.id)
    linked_ingredients = []
    for e in linked_entities:
        if isinstance(e, Ingredient):
            linked_ingredients.append(e)
    return linked_ingredients

def matched_linked_ingredients(ent1, ent2, recipe):
    """number of matched NOUN lemmas between the Ingredient entitied linking to
    ent1 and ent2"""
    linked_ing_ents = linked_ingredients(ent1, recipe)
    shared_lemmas = []
    for ent in linked_ing_ents:
        shared_lemmas.extend(shared_tokens(ent, ent2))
    return "matched_linked_ingredients", len(shared_lemmas) > 0

def matched_linked_ingredients_freq_sum(ent1, ent2, recipe):
    linked = linked_ingredients(ent1, recipe)
    freq_sum = 0
    for i in linked:
        freq_sum += shared_token_freq_sum(i, ent2, recipe)
    return "matched_linked_ingredients_freq_sum", freq_sum

def shared_nouns(entity1, entity2):
    ent1_lemmas = entity1.lemmas
    ent2_lemmas = entity2.lemmas
    shared_nouns = []
    for i in range(len(ent1_lemmas)):
        for j in range(len(ent2_lemmas)):
            if entity1.pos_simple[i] == 'NOUN' and \
                    entity2.pos_simple[j] == 'NOUN' and \
                    ent1_lemmas[i] == ent2_lemmas[j]:
                shared_nouns.append(ent1_lemmas[i])
    return shared_nouns

def shared_tokens(entity1, entity2):
    ent1_lemmas = entity1.lemmas
    ent2_lemmas = entity2.lemmas
    shared = []
    for i in range(len(ent1_lemmas)):
        for j in range(len(ent2_lemmas)):
            if ent1_lemmas[i] == ent2_lemmas[j]:
                shared.append(ent1_lemmas[i])
    return shared

def shared_token_freq_sum(entity1, entity2, recipe):
    shared = shared_tokens(entity1, entity2)
    freq_sum = 0
    for l in shared:
        freq_sum += lemma_frequency_in_instructions(l, recipe)
    return freq_sum

def have_shared_lemma(entity1, entity2, recipe):
    match = False
    for i in range(len(entity1.lemmas)):
        for j in range(len(entity2.lemmas)):
            if entity1.lemmas[i] == entity2.lemmas[j]:
                print(entity1.lemmas[i])
                match = True
    return "have_shared_lemma", match

def lemma_frequency_in_instructions(lemma, recipe):
    ins_entities = recipe.get_ins_entities()
    match_count = 0
    for e in ins_entities:
        for l in e.lemmas:
            if lemma == l:
                match_count += 1
    return 1.0/(match_count*match_count)

def preceding_action(ent, recipe):
    potential_action = None
    entities = recipe.get_ins_entities()
    for e in entities:
        if e is ent:
            return potential_action
        elif isinstance(e, Action):
            potential_action = e
    return potential_action

def num_matched_preceding_action_ingredients(ent1, ent2, recipe):
    prev_act = preceding_action(ent1, recipe)
    if prev_act:
        num_matched = num_matched_linked_ingredients(prev_act, ent2, recipe)[1]
        return "num_matched_preceding_action_ingredients", num_matched
    else:
        return "num_matched_preceding_action_ingredients", 0
            
def matched_preceding_action_ingredients(ent1, ent2, recipe):
    prev_act = preceding_action(ent1, recipe)
    matched = False
    if prev_act:
        matched = matched_linked_ingredients(prev_act, ent2, recipe)[1]
    return "matched_preceding_action_ingredients", matched

