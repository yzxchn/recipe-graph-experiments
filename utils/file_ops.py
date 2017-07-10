"""Functions used for file-related operations
"""
import os


def find_files_in_dir(top, extension=".xml"):
    """Find all the files ending with parameter extension in the given 
    directory, including subdirectories.
    """
    result = []
    dir_list = os.walk(top)
    for r,_,files in dir_list:
        for f in files:
            if f.endswith(extension):
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

def divide_files(files, train_ratio, test_ratio):
    """Divide items in files by train_ratio, test_ratio, and treat 
    remaining items as dev test files.
    """
    if (train_ratio + test_ratio) > 1:
        raise Exception("Train + Test ratio must be less than 1")
    size = len(files)
    train_num = int(size*train_ratio)
    test_num = int(size*test_ratio)
    dev_num = size - train_num - test_num
    train_end_index = train_num+1
    test_end_index = train_end_index+test_num
    return files[:train_end_index], files[train_end_index:test_end_index],\
                                    files[test_end_index:]

