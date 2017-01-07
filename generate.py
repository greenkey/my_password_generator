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

def format_error(error_text):
    return '--Error: ' + error_text


def run(argv=None):
    dictionary_filename = DEFAULT_DICTIONARY_FILENAME

    for arg in argv or []:
        if arg.startswith('dictionary='):
            dictionary_filename = arg.split('=')[1]
        if arg.startswith('import='):
            try:
                with open(arg.split('=')[1], 'r') as fi: #TODO: handle exception
                    with open(DEFAULT_DICTIONARY_FILENAME, 'a') as fo:
                        fo.write(fi.read())
            except FileNotFoundError:
                return format_error(f'Import file does not exists')
            return ''
        if arg.startswith('remove_from_dictionary=hard_to_digit'):
            return remove_from_dictionary(dictionary_filename)
    try:
        with open(dictionary_filename) as f:
            dictionary = f.read().split('\n')
    except FileNotFoundError:
        return format_error(f'Dictionary file does not exists: {dictionary_filename}')

    words = set()
    while len(words) < 4 and len(dictionary) > 0:
        word = dictionary.pop(random.randrange(len(dictionary))).strip()
        if word:
            words.add(word)

    return ' '.join(words)

if __name__ == '__main__':
    print(run(sys.argv))