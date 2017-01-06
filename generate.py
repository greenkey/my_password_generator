#!/usr/bin/env python3.6

import sys, random

DEFAULT_DICTIONARY_FILENAME = 'dictionary.txt'

def run(argv=None):
    dictionary_filename = DEFAULT_DICTIONARY_FILENAME

    for arg in argv or []:
        if 'dictionary=' in arg:
            dictionary_filename = arg.split('=')[1]

    try:
        with open(dictionary_filename) as f:
            dictionary = f.read().split('\n')
    except FileNotFoundError:
        return f'--Error: Dictionary file does not exists: {dictionary_filename}'

    words = set()
    while len(words) < 4:
        words.add(random.choice(dictionary))

    return ' '.join(words)

if __name__ == '__main__':
    print(run(sys.argv))