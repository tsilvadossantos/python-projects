def read_file(filename):
    data_loaded = []
    try:
        with open(filename, 'r') as r:
            for lines in r:
                data_loaded.append(lines.strip())
        return data_loaded
    except:
        print ('Error reading file: ',filename)
    return False

def write_to_file(filename, data, mode):
    f = open(filename, mode)
    f.write(data)
    f.close
