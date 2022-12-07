# import json

max_size1 = 100000


def index_nested_dict(dictionary: dict, keys: list):
    for key in keys:
        dictionary = dictionary[key]
    return dictionary


def build_filesystem():
    f = open("./input.txt", "r")
    current_path = []
    file_system = {'/': {}}
    for line in f:
        # print(line)
        if line.startswith("$ cd "):
            directory = line[5:].strip()
            if directory == "..":
                current_path.pop()
            elif directory == "/":
                current_path = ["/"]
            else:
                current_dir = index_nested_dict(file_system, current_path)
                current_path.append(directory)
                current_dir[directory] = {}
            # print(current_path)
        elif not line.startswith("$ ls"):
            if not line.startswith("dir"):
                file = line.split()
                fileSize = file[0]
                fileName = file[1]
                # print("file size", fileSize, "file name", fileName)
                current_dir = index_nested_dict(file_system, current_path)
                current_dir[fileName] = int(fileSize)
    return file_system


def dir_size(fs: dict):
    total_size = 0

    # problem asks for sum of all dirs less than 100k
    bellow_max_sum = 0
    for key, val in fs.items():

        if type(val) == dict:
            dsize, d_bellow_max_size = dir_size(val)
            total_size += dsize
            bellow_max_sum += d_bellow_max_size
            print('dir', key, 'size', dsize)
            if dsize <= max_size1:
                bellow_max_sum += dsize
        else:
            total_size += val
        print(key, type(val), "below_max_size", bellow_max_sum)
    return total_size, bellow_max_sum


def solution_part1():
    file_system = build_filesystem()
    # print(json.dumps(file_system, indent=4))
    dir_size(file_system)


solution_part1()
