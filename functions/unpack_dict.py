# Unpack Dictionary


# Unpack stmt_essential_dict items into CSV.
def unpack_dict(hints_enabled: bool, stmt_essential_dict: dict) -> list:
    keyval_pair = []
    for key, value in stmt_essential_dict.items():
        keyval_pair.append((key, value))
    if hints_enabled:
        print('\nHINT:',unpack_dict)
        for i in keyval_pair:
            print('HINT: unpacking', i)
    print() # white space
    return keyval_pair


if __name__ == '__main__':
    unpack_dict(True, None)