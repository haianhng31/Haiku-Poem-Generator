"""Check syllable-counting program against training corpus for haiku."""

import count_syllables
import sys

with open('train.txt') as f:
    words = set(f.read().split())

missing = []

for word in words:
    try:
        num_sys = count_syllables.count_syllable(word)
    except KeyError:
        missing.append(word)

if missing:
    print('Missing words:',missing,file=sys.stderr)
else:
    print('No word is missing.')