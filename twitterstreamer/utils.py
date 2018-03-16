def file_lines_to_array(fname):
    with open(fname) as f:
        arr = f.readlines()
        arr = [x.strip() for x in arr]
        return arr
