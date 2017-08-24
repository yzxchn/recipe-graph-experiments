from nltk.metrics import edit_distance
from nltk.corpus import wordnet as wn
import spacy

nlp = spacy.load('en')

def last_noun_index(entity, beg):
    while beg >= 0:
        if entity.pos_simple[beg] == "NOUN":
            break
        beg -= 1
    return beg

def last_noun(entity, beg):
    last_index = last_noun_index(entity, beg)
    return entity.lemmas[last_index] if last_index >= 0 else ""

def noun_index_before_comma(entity):
    last = len(entity.lemmas)
    for i in range(last):
        if entity.pos[i] == ',':
            last = i
    i = last - 1
    return last_noun_index(entity, i)

def noun_lemma_before_comma(entity1):
    """The NOUN lemma most immediately before a comma in an ingredient listing, 
    if there's any. 
    """
    ent1_last = ""
    last_index = noun_index_before_comma(entity1)
    if last_index >= 0:
        ent1_last = entity1.lemmas[last_index]
    return ent1_last

def get_noun_synsets(word):
    synsets = wn.synsets(word, pos=wn.NOUN)
    return synsets

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

def shared_lemmas(entity1, entity2):
    ent1_lemmas = entity1.lemmas
    ent2_lemmas = entity2.lemmas
    shared_lemmas = []
    for i in range(len(ent1_lemmas)):
        for j in range(len(ent2_lemmas)):
            if ent1_lemmas[i] == ent2_lemmas[j]:
                shared_lemmas.append(ent1_lemmas[i])
    return shared_lemmas


def noun_token_distance(entity1, entity2, recipe):
    """The Levenshtein distance between the last NOUN tokens in each of the 
    entities.
    """
    ent1_last = ""
    ent2_last = ""
    i = len(entity1.tokens) - 1
    j = len(entity2.tokens) - 1
    while i >= 0:
        if entity1.pos_simple[i] == "NOUN":
            ent1_last = entity1.tokens[i]
            break
        i -= 1
    while j >= 0:
        if entity2.pos_simple[j] == "NOUN":
            ent2_last = entity2.tokens[j]
            break
        j -= 1
    return "last_noun_token_distance", edit_distance(ent1_last, ent2_last)

def noun_lemma_distance(entity1, entity2, recipe):
    """The Levenshtein distance between the last NOUN lemmas in each of the 
    entities.
    """
    i = len(entity1.lemmas) - 1
    j = len(entity2.lemmas) - 1
    ent1_last = last_noun(entity1, i)
    ent2_last = last_noun(entity2, j)

    return "last_noun_token_distance", edit_distance(ent1_last, ent2_last)

def nl_before_comma_distance(entity1, entity2, recipe):
    """The Levenshtein distance between the last NOUN lemma before a comma for
    entity1, and the last NOUN lemman in entity2."""
    j = len(entity2.lemmas) - 1
    ent1_last = noun_lemma_before_comma(entity1)
    ent2_last = last_noun(entity2, j)

    return "last_noun_token_distance", edit_distance(ent1_last, ent2_last)

def nl_before_comma_wn_distance(entity1, entity2, recipe):
    """The max wordnet similarity score between the last noun lemma before a
    comma in entity1 and the last noun in entity2"""
    j = len(entity2.lemmas) - 1
    ent1_last = noun_lemma_before_comma(entity1)
    ent2_last = last_noun(entity2, j)
    ent1_synsets = get_noun_synsets(ent1_last)
    ent2_synsets = get_noun_synsets(ent2_last)
    max_similarity = 0
    for ent1_syn in ent1_synsets:
        for ent2_syn in ent2_synsets:
            similarity = ent1_syn.path_similarity(ent2_syn)
            if similarity > max_similarity:
                max_similarity = similarity
    return "max_wn_path_similarity", max_similarity
    
def nl_before_comma_wn_wup_distance(entity1, entity2, recipe):
    """The max wordnet similarity score between the last noun lemma before a
    comma in entity1 and the last noun in entity2"""
    j = len(entity2.lemmas) - 1
    ent1_last = noun_lemma_before_comma(entity1)
    ent2_last = last_noun(entity2, j)
    ent1_synsets = get_noun_synsets(ent1_last)
    ent2_synsets = get_noun_synsets(ent2_last)
    max_similarity = 0
    for ent1_syn in ent1_synsets:
        for ent2_syn in ent2_synsets:
            similarity = ent1_syn.wup_similarity(ent2_syn)
            if similarity > max_similarity:
                max_similarity = similarity

    return "max_wn_path_similarity", max_similarity

def nl_before_comma_vector_similarity(entity1, entity2, recipe):
    """The vector similarity score between the last noun lemma before a
    comma in entity1 and the last noun in entity2"""
    j = len(entity2.lemmas) - 1
    ent1_last = noun_lemma_before_comma(entity1)
    ent2_last = last_noun(entity2, j)
    ent1_last_v = nlp(ent1_last)
    ent2_last_v = nlp(ent2_last)
    
    return "nl_before_comma_vector_similarity", \
            ent1_last_v.similarity(ent2_last_v)

def noun_compound_distance(entity1, entity2, recipe):
    """The Levenshtein distance between the last noun compounds (the max span
    of text where all tokens are NOUNs)"""
    ent1_last = ""
    ent2_last = ""
    i = len(entity1.lemmas) - 1
    j = len(entity2.lemmas) - 1
    while i >= 0:
        if entity1.pos_simple[i] == "NOUN":
            ent1_last = entity1.lemmas[i]+" "+ent1_last
            if i - 1 < 0 or entity1.pos_simple[i-1] != "NOUN":
                break
        i -= 1
    while j >= 0:
        if entity2.pos_simple[j] == "NOUN":
            ent2_last = entity2.lemmas[j]
            if j - 1 < 0 or entity2.pos_simple[j-1] != "NOUN":
                break
        j -= 1
    return "last_noun_compound_distance", edit_distance(ent1_last, ent2_last)

def num_unigram_matches(entity1, entity2, recipe):
    """The number of matched tokens between the two entities.
    """
    pass

def num_noun_lemma_matches(entity1, entity2, recipe):
    """The number of matched NOUN lemmas between the two entities.
    """
    return "num_shared_nouns", len(shared_nouns(entity1, entity2))

def max_match_from_last_noun(entity1, entity2):
    """The maximum number of matched lemmas from the last noun before comma in 
    entity1 and the last noun in entity2"""
    e1_last_n = noun_index_before_comma(entity1)
    e2_last_n = last_noun_index(entity2, len(entity2.lemmas)-1)
    matched = []
    while e1_last_n >= 0 and e2_last_n >= 0 and \
          entity1.lemmas[e1_last_n] == entity2.lemmas[e2_last_n]:
        matched.append(entity1.lemmas[e1_last_n])
        e1_last_n -= 1
        e2_last_n -= 1
    matched_lemmas = list(reversed(matched))
    return matched_lemmas

def max_match_size(entity1, entity2, recipe):
    return len(max_match_from_last_noun(entity1, entity2))

def lemma_frequency_in_instructions(lemma, recipe):
    ins_entities = recipe.get_ins_entities()
    match_count = 0
    for e in ins_entities:
        for l in e.lemmas:
            if lemma == l:
                match_count += 1
    return 1.0/(match_count*match_count)


def max_match_frequency_sum(entity1, entity2, recipe):
    max_match = max_match_from_last_noun(entity1, entity2)
    freq_sum = 0
    for l in max_match:
        freq_sum += lemma_frequency_in_instructions(l, recipe)
    return "max_match_frequency_sum", freq_sum

def lemma_match_frequency_sum(entity1, entity2, recipe):
    max_match = shared_lemmas(entity1, entity2)
    freq_sum = 0
    for l in max_match:
        freq_sum += lemma_frequency_in_instructions(l, recipe)
    return "lemma_match_frequency_sum", freq_sum
    

def contain_measurement(entity1, entity2, recipe):
    """Whether entity2 contain measurement information, such as numbers.
    """
    return "contain_measurement", "NUM" in entity2.pos_simple

def freq_sum_inst_position_similarity(entity1, entity2, recipe):
    relative_inst_pos = entity2.sent_i*1.0/recipe.ins_num_lines
    return "freq_sum_inst_position_similarity", 1 -\
             abs(lemma_match_frequency_sum(entity1, entity2, recipe)[1] - \
                   relative_inst_pos)

def relative_position_similarity(entity1, entity2, recipe):
    relative_ing_pos = entity1.sent_i*1.0/recipe.ing_num_lines
    relative_ins_pos = entity2.sent_i*1.0/recipe.ins_num_lines

    return "relative_position_similarity", 1 - abs(relative_ing_pos - \
                                                   relative_ins_pos)


class FeatureExtractor:
    def __init__(self, feature_functions=[]):
        self.feature_functions = feature_functions

    def add_feature_function(self, feature_function):
        self.feature_functions.append(feature_function)

    def extract_features(self, entity_pairs, recipes):
        """Extract features from samples.
        entity_pairs: a list of tuples of two Entity objects.
        recipes: a list of RecipeReader objects
        len(entity_pairs) should equal len(recipes), each pair of entities 
        correspond to a recipe object they are in.
        """
        samples = zip(entity_pairs, recipes)
        features = []
        for pair, recipe in samples:
            entity1, entity2 = pair
            feature_set = {}
            for f in self.feature_functions:
                feature_name, feature_value = f(entity1, entity2, recipe)
                feature_set[feature_name] = feature_value
            features.append(feature_set)
        return features
    
