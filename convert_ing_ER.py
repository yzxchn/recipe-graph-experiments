#!/usr/bin/env python3

"""Converts dataset into CRFSuite-readable format, and divide into train, test 
and test sets.
"""

if __name__ == "__main__":

    from utils import file_ops
    import sys, os
    import random

    # define what each item in a line in a src file is
    line_pattern = "id beg end txt pos".split()
    output_pattern = "txt pos".split()

    src_dir, dst_dir = sys.argv[1:3]
    train_ratio, test_ratio = map(float, sys.argv[3:])
    # Find all files ending with .ient in the src directory
    src_paths = file_ops.find_files_in_dir(src_dir, '.ient')

    # Set seed to 1 for testing
    random.seed(1)
    random.shuffle(src_paths)

    train, test, dev = file_ops.divide_files(src_paths, train_ratio, test_ratio)
    for f in train:
        file_name = os.path.basename(f)
        file_ops.convert_to_crfsuite(f,os.path.join(dst_dir, "train", 
                                                    file_name), 
                                     line_pattern, 
                                     output_pattern)
    for f in test:
        file_name = os.path.basename(f)
        file_ops.convert_to_crfsuite(f,os.path.join(dst_dir, "test", file_name), 
                                     line_pattern, 
                                     output_pattern)
    for f in dev:
        file_name = os.path.basename(f)
        file_ops.convert_to_crfsuite(f,os.path.join(dst_dir, "dev", file_name), 
                                     line_pattern, 
                                     output_pattern)
