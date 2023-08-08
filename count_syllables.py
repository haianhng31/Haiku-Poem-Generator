import sys
from string import punctuation
import json
from nltk.corpus import cmudict

# load dictionary of words in haiku corpus but not in cmudict
with open('missing_words.json') as f:
    missing_words = json.load(f)
    #read the content of the JSON file and load it as Python data.
    # In this case, the content of the "missing_words.json" file is a JSON array,
    # and the function will convert that JSON array into a Python list or dictionary,
    # depending on the JSON content.

cmudict = cmudict.dict()

def count_syllable(words):
    num_syl = 0
    words = words.strip(punctuation).replace('-', ' ').replace("'s", ' ').replace("’s", ' ').lower().split()
    for word in words:
        if word in missing_words:
            num_syl += missing_words[word]
        else:
            for phonemes in cmudict[word][0]: #[0] indexing selects the first pronunciation from the list (often referred to as the primary pronunciation)
                for phoneme in phonemes:
                    # checks if the last character of the sound is a digit (0-9).
                    # In the CMU Pronouncing Dictionary, digits are used to represent stress levels of syllables
                    if phoneme[-1].isdigit():
                        num_syl += 1

    return num_syl

def main():
    word = input('Enter word or phrase else press Enter to exit: ')
    if word == "":
        sys.exit()
    try:
        num_syl = count_syllable(word)
        print(f'Number of syllables in {word} is {num_syl}')
        print()
    except KeyError:
        # KeyError: the word was not found in the data structure or dictionary being used
        # in the count_syllable function
        print('Word not found. Try again.\n',file = sys.stderr)

if __name__ == '__main__':
    main()