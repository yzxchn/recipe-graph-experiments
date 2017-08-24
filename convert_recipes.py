#!/usr/bin/env python3
import spacy, os

nlp = spacy.load("en")

def ingredient_pos_align(text, offset=0):
    """Align tokens in the ingredients section with their POS and 
    indexes in the original annotated recipe.
    """
    i = 0
    lines = text.split('\n')
    tokens = []
    for line in lines:
        line_tokens = []
        processed_line = nlp(line)
        for w in processed_line:
            beg, i = find_token_position(w.text, text, i)
            line_tokens.append((w.text,
                                w.lemma_,
                                w.tag_, 
                                w.pos_, 
                                w.dep_,
                                w.head.text,
                                w.head.lemma_,
                                w.head.tag_,
                                w.head.pos_,
                                w.head.dep_,
                                w.head.head.text,
                                w.head.head.lemma_,
                                w.head.head.tag_,
                                w.head.head.pos_,
                                w.head.head.dep_,
                                (beg+offset, i+offset)))
        tokens.append(line_tokens) 
    return tokens

def instruction_pos_align(text, offset=0):
    """Align tokens in the instructions section with their POS and indexes 
    in the original annotated recipe.
    """
    i = 0
    doc = nlp(text)
    tokens = []
    for sent in doc.sents:
        sent_tokens = []
        for w in sent:
            beg, i = find_token_position(w.text, text, i)
            sent_tokens.append((w.text,
                                w.lemma_,
                                w.tag_, 
                                w.pos_, 
                                w.dep_,
                                w.head.text,
                                w.head.lemma_,
                                w.head.tag_,
                                w.head.pos_,
                                w.head.dep_,
                                w.head.head.text,
                                w.head.head.lemma_,
                                w.head.head.tag_,
                                w.head.head.pos_,
                                w.head.head.dep_,
                                (beg+offset, i+offset)))
        tokens.append(sent_tokens)
    return tokens

def format_output(*args):
    """Joining arguments into one line, each separated by a tab
    """
    def convert_to_str(arg):
        """Convert argument to string, if argument is a whitespace character,
        convert it to a space.
        """
        arg = str(arg)
        if arg.isspace():
            return " "
        else:
            return arg
    return '\t'.join(map(convert_to_str, args))

def find_token_position(token, text, start):
    """
    Returns the range of index in text where the token is.
    
    token: a token contained in the text
    start: the starting index to look for the token.
    
    """
    i = start
    while text[i] != token[0] or text[i+len(token)-1] != token[-1]:
        if not text[i].isspace():
            raise Exception("Token does not match text in position")
        i += 1
    return i, i+len(token)

if __name__ == "__main__":
    import sys
    from recipe_reader.recipe_reader import AnnotatedRecipe
    from recipe_reader.annotation_tags import *
    from utils import file_ops
    """
    For each annotated recipe in the given directory, pos tag its instructions 
    part and output each token, POS of the token, and the range in the text for 
    that token

    Commandline arguments:
    file_directory: the root directory of all the annotated XML recipes
    ing_entity_directory: the root directory to output files containing 
                          ingredient entity tags.
    instruct_entity_directory: the root directory to output files containing 
                               instruction entity tags
    link_directory: the root directory to output files containing link tags
    """
    file_directory = sys.argv[1]
    ing_entity_directory, instruct_entity_directory = sys.argv[2], sys.argv[3]
    link_directory = sys.argv[4]
    atts_directory = sys.argv[5]
    file_paths = file_ops.find_files_in_dir(file_directory)
    for f in file_paths:
        parents, base = os.path.split(f)
        base_name = os.path.splitext(base)[0]
        ing_ent_out_name = base_name + ".ient"
        ent_out_name = base_name +".entity"
        link_out_name = base_name + ".link"
        atts_out_name = base_name + ".atts"
        # output files maintain the same directory structure (organized by 
        # source website) as the input files
        ing_ent_out_path = os.path.join(ing_entity_directory, 
                                        file_ops.truncate_path(parents, 1), 
                                        ing_ent_out_name)
        ent_out_path = os.path.join(instruct_entity_directory, 
                                    file_ops.truncate_path(parents, 1), 
                                    ent_out_name)
        link_out_path = os.path.join(link_directory, 
                                     file_ops.truncate_path(parents, 1), 
                                     link_out_name)
        atts_out_path = os.path.join(atts_directory, 
                                     file_ops.truncate_path(parents, 1), 
                                     atts_out_name)

        with open(ing_ent_out_path,'w') as ing_ent_out,\
            open(ent_out_path, "w") as ent_out, \
            open(link_out_path, 'w') as link_out, \
            open(atts_out_path, 'w') as atts_out:
            doc = AnnotatedRecipe(f)
            instruct_tokens = instruction_pos_align(doc.get_instructions(), 
                                                    doc.instructions_beg)
            ing_tokens = ingredient_pos_align(doc.get_ingredients(), 
                                              doc.ingredients_beg)
            # tokens is a collection of lists of tokens, each list is
            # a sentence in the document
            for sent in instruct_tokens:
                for tok in sent:
                    text, lemma, tag, pos, dep = tok[:5]
                    ptext, plemma, ptag, ppos, pdep = tok[5:10]
                    pptext, pplemma, pptag, pppos, ppdep = tok[10:15]
                    range_ = tok[-1]
                    r_beg, r_end = range_
                    covering_entities = doc.get_covering_entities(r_beg, r_end)
                    covering_ids = '|'.join(covering_entities)
                    # use "-" when a token doesn't belong to any entity
                    if len(covering_ids) == 0:
                        covering_ids = '-'
                    ent_out.write(format_output(covering_ids,
                                                r_beg, r_end,
                                                text, lemma, tag, pos, dep,
                                                ptext, plemma, ptag, ppos, pdep,
                                                pptext, pplemma, pptag, 
                                                pppos, ppdep) +"\n")
                ent_out.write("\n")
            # find the entities in the ingredients section.
            for line in ing_tokens:
                for tok in line:
                    text, lemma, tag, pos, dep = tok[:5]
                    ptext, plemma, ptag, ppos, pdep = tok[5:10]
                    pptext, pplemma, pptag, pppos, ppdep = tok[10:15]
                    range_ = tok[-1]
                    r_beg, r_end = range_                    
                    covering_entities = doc.get_covering_entities(r_beg, r_end)
                    covering_ids = '|'.join(covering_entities)
                    if len(covering_ids) == 0:
                        covering_ids = '-'
                    ing_ent_out.write(format_output(covering_ids,
                                                r_beg, r_end,
                                                text, lemma, tag, pos, dep,
                                                ptext, plemma, ptag, ppos, pdep,
                                                pptext, pplemma, pptag, 
                                                pppos, ppdep) + "\n")
                ing_ent_out.write("\n")
            link_tags = doc.get_link_tags()
            for lt in link_tags:
                link_out.write(format_output(lt.get_id(), lt.first_id, 
                                                        lt.first_text,
                                                        lt.second_id,
                                                        lt.second_text))
                link_out.write('\n')

            # output attributes for Action and Ingredient tags.
            extent_tags = doc.get_extent_tags()
            for tag in extent_tags:
                if isinstance(tag, ActionTag):
                    atts_out.write(format_output(tag.get_id(), 
                                   tag.get_action_type()))
                elif isinstance(tag, IngredientTag):
                    atts_out.write(format_output(tag.get_id(), 
                                   tag.is_start_state(),
                                   tag.is_composite()))
                atts_out.write('\n')
