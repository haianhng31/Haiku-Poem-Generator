import count_syllables
import json
from nltk.corpus import cmudict
from string import punctuation
import test_count_syllables_w_dict
import random
from collections import Counter

with open('missing_words.json') as f:
    missing_words_file = json.load(f)
cmudict = cmudict.dict()
file = test_count_syllables_w_dict.load_file('2of4brif.txt')

def load_haiku(file):
    # Return a text file as a string
    # Load string, remove newline, split words on spaces, and return list.
    with open(file) as f:
        corpus = f.read().strip(punctuation).replace('\n',' ').lower().split()
        return corpus


def markov_model_1(corpus):
    markov_1 = {}
    corpus = list(corpus)
    for i in range(len(corpus) - 1):
        if corpus[i] not in markov_1.keys():
            markov_1[corpus[i]] = [corpus[i+1]]
        else:
            markov_1[corpus[i]].append(corpus[i+1])
    sorted_markov_1 = {word:markov_1[word] for word in sorted(markov_1)}
    return sorted_markov_1

def markov_model_2(corpus):
    markov_2 = {}
    corpus = list(corpus)
    for i in range(len(corpus) - 2):
        key = " ".join([corpus[i],corpus[i+1]])
        if key not in markov_2.keys():
            markov_2[key] = [corpus[i+2]]
        else:
            markov_2[key].append(corpus[i+2])
    sorted_markov_2 = {word:markov_2[word] for word in sorted(markov_2)}
    return sorted_markov_2

def main():
    training_corpus = load_haiku('train.txt') #process the training corpus for spaces, newline breaks...
    markov_1 = markov_model_1(training_corpus)
    print(markov_1)
    #markov_2 = markov_model_2(training_corpus)
    #print(markov_2)

    '''
    # Generate the 1st line
    syl_num = 0
    #while syl_num != 5:

    seed_word = random.choice(training_corpus)
    while count_syllables.count_syllable(seed_word) > 4:
        seed_word = random.choice(training_corpus)
    syl_num += count_syllables.count_syllable(seed_word)
    print(seed_word, syl_num)

    #seed_suffix = Counter(markov_1[seed_word]).most_common()
    seed_suffix = markov_1[seed_word][0]
    syl_num += count_syllables.count_syllable(seed_word)
    print(seed_suffix,syl_num)

    key = " ".join([seed_word, seed_suffix])
    #first_suffix = Counter(markov_2[key]).most_common()
    first_suffix = markov_2[key][0]
    syl_num += count_syllables.count_syllable(first_suffix)
    print(first_suffix,syl_num)


    

    # Give user choice of generating full Haiku, redoing line 2 or 3, or exiting
    choice = input('Enter "full" to generate your own full haiku, or "2" or "3" to redo line 2 or 3, or press Enter to exit: ')
    if choice == "":
        sys.exit()
    if choice == "2":
    if choice == "3":
    if choice == "full" '''

if __name__ == "__main__":
    main()

