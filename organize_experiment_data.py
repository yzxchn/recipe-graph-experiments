#!/usr/bin/env python3

from utils import file_ops
import os

def get_recipe_identifiers(recipe_ing_dir):
    """Get an identifier for a recipe. 
    An identifier is the recipe file name without the last extension, together 
    with 2 levels of directory names above. 
    Exmaple:
    allrecipes/1/amish_white_bread.txt

    recipe_dir: the path to the ing_entity folder in the data directory. 
    """
    # get all the files under the ing_entity directory.
    files = file_ops.find_files_in_dir(recipe_ing_dir, extension=".ient")
    result = []
    for f in files:
        truncated = file_ops.truncate_path(f, level=2)
        result.append(os.path.splitext(truncated)[0])
    return result

if __name__ == "__main__":
    import sys, shutil, random

    in_dir, out_dir = sys.argv[1:3]
    train_ratio, test_ratio = map(float, sys.argv[3:5])
    files = get_recipe_identifiers(in_dir)
    random.seed(1)
    random.shuffle(files)
    train, test, dev = file_ops.divide_files(files, 
                                             train_ratio, test_ratio)
    extensions = [".ient", ".entity", ".link", ".atts"]
    folders = ["ing_entity", "instruct_entity", "link", "atts"]
    datasets = ["train", "test", "dev"]
    for folder, ext in zip(folders, extensions):
        for dataset_name, dataset in zip(datasets, (train, test, dev)):
            for f in dataset:
                filename = file_ops.truncate_path(f)
                in_path = os.path.join("../data", folder, f+ext)
                out_path = os.path.join(out_dir, dataset_name, 
                                        folder, filename+ext)
                shutil.copyfile(in_path, out_path)
