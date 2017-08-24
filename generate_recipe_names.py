from utils import file_ops
import os

def get_recipe_identifiers(ing_dir):
    files = file_ops.find_files_in_dir(ing_dir, extension=".ient")
    result = []
    for f in files:
        truncated = file_ops.truncate_path(f, level=0)
        result.append(os.path.splitext(truncated)[0])
    return result

if __name__ == "__main__":
    import sys

    in_dir = sys.argv[1]

    names = get_recipe_identifiers(in_dir)

    for n in names:
        print(n)
