#!/usr/bin/env python3.6

import sys, random

DEFAULT_DICTIONARY_FILENAME = 'dictionary.txt'

def is_easy_to_digit(s):
    s = s.strip().lower()
    for i in range(len(s)-1):
        if sum([0 if l in 'yuiophjklnm' else 1 for l in s[i:i+2]]) != 1:
            return False
    return True

def remove_from_dictionary(dictionary=DEFAULT_DICTIONARY_FILENAME):
    with open(DEFAULT_DICTIONARY_FILENAME, 'r') as dictionary:
        words = dictionary.read().split('\n')

    newdict = set()
    for word in words:
        if is_easy_to_digit(word):
            newdict.add(word)

    with open(DEFAULT_DICTIONARY_FILENAME, 'w') as dictionary:
        dictionary.write('\n'.join(newdict))

    return ''


def run(argv=None):
    dictionary_filename = DEFAULT_DICTIONARY_FILENAME

    for arg in argv or []:
        if 'dictionary=' in arg:
            dictionary_filename = arg.split('=')[1]
        if 'import=' in arg:
            with open(arg.split('=')[1], 'r') as fi: #TODO: handle exception
                with open(DEFAULT_DICTIONARY_FILENAME, 'a') as fo:
                    fo.write(fi.read())
            return ''
        if 'remove_from_dictionary=hard_to_digit' in arg:
            return remove_from_dictionary(dictionary_filename)
    try:
        with open(dictionary_filename) as f:
            dictionary = f.read().split('\n')
    except FileNotFoundError:
        return f'--Error: Dictionary file does not exists: {dictionary_filename}'

    words = set()
    while len(words) < 4 and len(dictionary) > 0:
        words.add(dictionary.pop(random.randrange(len(dictionary))))

    return ' '.join(words)

if __name__ == '__main__':
    print(run(sys.argv))