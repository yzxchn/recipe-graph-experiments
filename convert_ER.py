#!/usr/bin/env python3

"""Converts dataset into CRFSuite-readable format, and divide into train, test 
and dev sets.
"""
import json
import os

label_map = json.load(open(os.path.join(os.path.dirname(__file__),
                                        'utils/label_map.json')))

def convert_to_crfsuite(src_path, dst_path, pattern, output_pattern):
    """Converts a file specified by src_path to CRFSuite-readable format.
    Each value in a line is specified by output_pattern
    """
    last_id = None
    with open(src_path) as src, open(dst_path, 'w') as dst:
        for line in src:
            line = line.strip('\n')
            # if current line is a line separator (empty line) in the src file
            if not line:
                dst.write('\n')
            else:
                output_values = []
                # map each value name in pattern to the respective value
                values = dict(zip(pattern, line.split('\t')))
                id_ = values["id"]
                if id_ == '-':
                    output_values.append('O')
                elif id_ == last_id:
                    output_values.append("I-{}".format(label_map[last_id[0].upper()]))
                else:
                    output_values.append("B-{}".format(label_map[id_[0].upper()]))
                last_id = id_
                # add corresponding values to the line as 
                # specified by output_pattern
                for out_name in output_pattern:
                    output_values.append(values[out_name])
                dst.write('\t'.join(output_values)+'\n')

if __name__ == "__main__":

    from utils import file_ops
    import sys, os
    import random

    # define what each item in a line in a src file is
    line_pattern = ("id beg end txt lemma tag pos dep "+\
                   "ptxt plemma ptag ppos pdep "+\
                   "pptxt pplemma pptag pppos ppdep").split()
    output_pattern = ("txt lemma tag pos dep "+\
                      "ptxt plemma ptag ppos pdep "+\
                      "pptxt pplemma pptag pppos ppdep").split()

    src_dir, file_extension, dst_dir = sys.argv[1:4]
    train_ratio, test_ratio = map(float, sys.argv[4:])
    # Find all files ending with .ient in the src directory
    src_paths = file_ops.find_files_in_dir(src_dir, file_extension)

    # Set seed to 1 for testing
    random.seed(1)
    random.shuffle(src_paths)

    train, test, dev = file_ops.divide_files(src_paths, train_ratio, test_ratio)
    for f in train:
        file_name = os.path.basename(f)
        convert_to_crfsuite(f,os.path.join(dst_dir, "train", 
                                           file_name), 
                            line_pattern, 
                            output_pattern)
    for f in test:
        file_name = os.path.basename(f)
        convert_to_crfsuite(f,os.path.join(dst_dir, "test", file_name), 
                            line_pattern, 
                            output_pattern)
    for f in dev:
        file_name = os.path.basename(f)
        convert_to_crfsuite(f,os.path.join(dst_dir, "dev", file_name), 
                            line_pattern, 
                            output_pattern)
