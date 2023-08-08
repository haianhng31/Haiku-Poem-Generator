import sys
from string import punctuation
#import nltk
from nltk.corpus import cmudict
import pprint
import json

cmudict = cmudict.dict()

def load_haiku(file):
    """Open and return training corpus of haiku as a set."""
    with open(file) as f:
        word_set = set(f.read().strip(punctuation).replace('-', ' ').replace("'s", ' ').replace("’s", ' ').lower().split())
        return word_set

def cmudict_missing(word_set):
    """Find and return words in word set missing from cmudict."""
    missing_words = set()
    for word in word_set:
        word = word.strip(punctuation)
        if word not in cmudict:
            missing_words.add(word)
    print('Missing words / Exceptions: ')
    print(*missing_words,sep='\n')
    print('\nNumber of unique words in haiku corpus = {}'.format(len(word_set)))
    print('Number of words in corpus not in cmudict = {}'.format(len(missing_words)))

    # the % of elements (words) in the word_set that are not in the exceptions collection
    membership = ((1 - len(missing_words))/len(word_set))*100
    # The {:.1f} display the membership value with one decimal point
    print('cmudict membership = {:.1f}'.format(membership,'%'))
    return missing_words

def add_num_syllables(exceptions):
    missing_words = {}
    print('\nInput # syllables in word. Mistakes can be corrected at end. \n')
    for word in exceptions:
        while True:
            num_syl = input('Enter number of syllables in {}: '.format(word))
            if num_syl.isalnum():
                break
            else:
                print(f'{num_syl} is not a valid answer. Try again',file=sys.stderr)
        missing_words[word] = int(num_syl)
    print()
    pprint.pprint(missing_words, width = 1)

    print("\nMake changes to dictionary before saving?")
    print("""
    0 - Exit & Save
    1 - Add a Word or Change a Syllable Count 
    2 - Remove a Word""")
    while True:
        choice = input('\nEnter choice? ')
        if choice =="0":
            break
        if choice == "1":
            word = input('Type a word to add or change its Syllable Count: ')
            missing_words[word] = int(input(f"{word}'s Syllable Count: "))
        if choice == "2":
            word = input('Type a word to remove')
            missing_words.pop(word,None)

    print("\nNew words or syllable changes:")
    pprint.pprint(missing_words, width=1)

    return missing_words

def save_exceptions(word_dict):
    """Save exceptions dictionary as json file."""
    json_string = json.dumps(word_dict)

    f = open('missing_words.json','w')
    #opens a new file named "missing_words.json" in write mode ('w').
    # If the file does not exist, it will be created.
    # If the file already exists, its contents will be overwritten.

    f.write(json_string)
    f.close()
    print("\nFile saved as missing_words.json")

def main():
    haiku = load_haiku('train.txt')
    exceptions = cmudict_missing(haiku)
    build_dict = input('\nManually build an exceptions dictionary (y/n)? ' )
    if build_dict.lower() == "n":
        sys.exit()
    else:
        missing_words_dict = add_num_syllables(exceptions)
        save_exceptions(missing_words_dict)

if __name__ == '__main__':
    main()