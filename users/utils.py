

def split_name(full_name):
    names = full_name.split()
    first_name = names[0]
    last_name = ' '.join(names[1:]) if len(names) > 1 else ''
    return first_name, last_name


