#!/usr/bin/env python3
import spacy, os

nlp = spacy.load("en")

def pos_align(text, offset=0):
    i = 0
    doc = nlp(text)
    tokens = []
    for sent in doc.sents:
        sent_tokens = []
        for w in sent:
            beg, i = find_token_position(w.text, text, i)
            sent_tokens.append((w.text, w.pos_, (beg+offset, i+offset)))
        tokens.append(sent_tokens)
    return tokens

def format_output(*args):
    """Joining arguments into one line, each separated by a tab
    """
    return '\t'.join(map(str, args))

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

def find_files_in_dir(top, extension=".xml"):
    result = []
    dir_list = os.walk(top)
    for r,_,files in dir_list:
        for f in files:
            result.append(os.path.join(r, f))
    return result

def truncate_path(path, level=0):
    """
    Truncate the given path, keeping level number of parent directory names.

    path: a path to a file or directory
    level: number of levels of parent directories to be kept
    """
    parent, base = os.path.split(path)
    if level <= 0:
        return base
    else:
        return os.path.join(truncate_path(parent, level=level-1), base)

if __name__ == "__main__":
   import sys
   from recipe_reader import AnnotatedRecipe
   """
   For each annotated recipe in the given directory, pos tag its instructions 
   part and output each token, POS of the token, and the range in the text for 
   that token
   """
   file_directory, output_directory = sys.argv[1:]
   file_paths = find_files_in_dir(file_directory)
   for f in file_paths:
       parents, base = os.path.split(f)
       out_name = os.path.splitext(base)[0]+".pos"
       out_path = os.path.join(output_directory, 
                               truncate_path(parents, 1), out_name)
       with open(out_path, "w") as out:
           doc = AnnotatedRecipe(f)
           tokens = pos_align(doc.get_instructions(), doc.instructions_beg)
           # tokens is a collection of lists of tokens, each list is
           # a sentence in the document
           for sent in tokens:
               for tok in sent:
                   text, pos, range_ = tok
                   r_beg, r_end = range_
                   covering_ids = '|'.join(doc.get_covering_entities(r_beg, 
                                                                     r_end))
                   if len(covering_ids) == 0:
                       covering_ids = '-'
                   out.write(format_output(covering_ids, text, pos, r_beg, r_end)
                             +"\n")
               out.write("\n")
