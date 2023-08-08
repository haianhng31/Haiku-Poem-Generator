import sys
from collections import defaultdict
from string import punctuation
import logging
import random
import count_syllables

# !!!
logging.disable(logging.CRITICAL)  # comment-out to enable debugging messages
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def load_training_file(file):
    # Return a text file as a string
    with open(file) as f:
        raw_haiku = f.read()
        # When you call read() on a file object,
        # it reads the contents of the file and returns them as a single string.
        return raw_haiku

def prep_training(raw_haiku):
    # Load string, remove newline, split words on spaces, and return list.
    # !!!
    # translator = str.maketrans('', '', punctuation)
    # corpus = raw_haiku.replace('\n',' ').translate(translator).split()
    corpus = raw_haiku.replace('\n', ' ').split()
    return corpus

def map_word_to_word(corpus):
    dict_1to1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < (len(corpus) - 1):
            dict_1to1[word].append(corpus[index+1])
    logging.debug("map_word_to_word results for \"sake\" = %s\n",
                  dict_1to1['sake']) #!!!
    return dict_1to1

def map_2_words_to_word(corpus):
    dict_2to1 = defaultdict(list)
    for i in range(len(corpus)):
        if i < (len(corpus) - 2):
            key = " ".join([corpus[i],corpus[i+1]])
            dict_2to1[key].append(corpus[i+2])
    logging.debug("map_2_words_to_word results for \"sake jug\" = %s\n",
                  dict_2to1['sake jug']) #!!!
    return dict_2to1

def random_word(corpus):
    word = random.choice(corpus)
    num_syls = count_syllables.count_syllable(word)
    if num_syls > 4:
        random_word(corpus)
    else:
        logging.debug("random word & syllables = %s %s\n", word, num_syls)
        return (word, num_syls)

def word_after_single(prefix,suffix_map_1,line_syls,target_syls):
    # Return all acceptable words in a corpus that follow a single word.
    word_choices = []
    suffixes = suffix_map_1.get(prefix)
    if suffixes != None:
        for candidate in suffixes:
            num_syls = count_syllables.count_syllable(candidate)
            if num_syls + line_syls <= target_syls:
                word_choices.append(candidate)
    logging.debug("accepted words after \"%s\" = %s\n",
                  prefix, set(word_choices))
    return word_choices

def word_after_double(prefix, suffix_map_2, line_syls,target_syls):
    word_choices = []
    suffixes = suffix_map_2.get(prefix)
    if suffixes != None:
        for candidate in suffixes:
            num_syls = count_syllables.count_syllable(candidate)
            if num_syls + line_syls <= target_syls:
                word_choices.append(candidate)
    logging.debug("accepted words after \"%s\" = %s\n",
                  prefix, set(word_choices))
    return word_choices

def haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line, target_syls):
    # Build a haiku line from a training corpus and return it.
    line = '2/3'
    line_syls = 0
    current_line = []

    if len(end_prev_line) == 0: #build first line
        line = '1'
        # First word
        word, num_syls = random_word(corpus)
        current_line.append(word)
        line_syls += num_syls

        # 2nd word
        next_word_choices = word_after_single(word, suffix_map_1, line_syls, target_syls)
        while len(next_word_choices) == 0:
            prefix = random_word(corpus)
            logging.debug("new random prefix = %s", prefix)
            next_word_choices = word_after_single(prefix, suffix_map_1, line_syls, target_syls)

        word = random.choice(next_word_choices)
        num_syls = count_syllables.count_syllable(word)
        logging.debug("word & syllables = %s %s", word, num_syls)
        current_line.append(word)
        line_syls += num_syls

        if line_syls == target_syls:
            end_prev_line.extend(current_line[-2:])
            #selects the last two elements
            #extend() method is used to add multiple elements to a list.
            return current_line, end_prev_line

    else: #build line 2 & 3
        current_line.extend(end_prev_line)

    while True:
        logging.debug("line = %s\n", line)
        prefix = current_line[-2] + " " + current_line[-1]
        next_word_choices = word_after_double(prefix, suffix_map_2, line_syls, target_syls)
        while len(next_word_choices) == 0:
            index = random.randint(0, len(corpus) - 2)
            prefix = corpus[index] + " " + corpus[index+1]
            next_word_choices = word_after_double(prefix, suffix_map_2, line_syls, target_syls)
        word = random.choice(next_word_choices)
        num_syls = count_syllables.count_syllable(word)
        logging.debug("word & syllables = %s %s", word, num_syls)

        if line_syls + num_syls > target_syls:
            continue
            #continue statement is used in loops (like for or while)
            # to skip the rest of the loop's body & move to the next iteration of the loop.
        elif line_syls + num_syls < target_syls:
            current_line.append(word)
            line_syls += num_syls
        elif line_syls + num_syls == target_syls:
            current_line.append(word)
            break

    if line == '1':
        final_line = current_line[:]
        # we need the [:] so that final_line is an independent list,
        # any changes made to final_line will not affect current_line, and vice versa

    if line == '2/3':
        final_line = current_line[2:]

    return final_line, end_prev_line

def main():
    """Give user choice of building a haiku or modifying an existing haiku."""
    intro = """\n
    A thousand monkeys at a thousand typewriters...
    or one computer...can sometimes produce a haiku.\n"""
    print("{}".format(intro))

    raw_haiku = load_training_file('train.txt')
    corpus = prep_training(raw_haiku)
    suffix_map_1 = map_word_to_word(corpus)
    suffix_map_2 = map_2_words_to_word(corpus)
    final = []

    choice = None
    while choice != "0":
        print(
            """
            Japanese Haiku Generator

            0 - Quit
            1 - Generate a Haiku poem
            2 - Regenerate Line 2
            3 - Regenerate Line 3
            """
        )

        choice = input('Choice? ')
        print()

        #exit
        if choice == "0":
            print('Sayonara.')
            sys.exit()

        # generate a full haiku
        elif choice == "1":
            final = []
            end_prev_line = []
            first_line, end_prev_line1 = haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line, 5)
            final.append(first_line)
            line, end_prev_line2 = haiku_line(suffix_map_1, suffix_map_2, corpus, end_prev_line1, 7)
            final.append(line)
            line, end_prev_line3 = haiku_line(suffix_map_1, suffix_map_2,
                                              corpus, end_prev_line2, 5)
            final.append(line)

        elif choice == '2':
            if not final:
                print('Please generate a full Haiku first (Option 1).')
                continue
            else:
                line, end_prev_line2 = haiku_line(suffix_map_1, suffix_map_2,
                                                  corpus, end_prev_line1, 7)
                final[1] = line

        elif choice == '3':
            if not final:
                print('Please generate a full Haiku first (Option 1).')
                continue
            else:
                line, end_prev_line3 = haiku_line(suffix_map_1,suffix_map_2,corpus,end_prev_line2, 5)
                final[2] = line

        # some unknown choice
        else:
            print('\nSorry. This is not a valid choice. Choose again.')
            continue

        # Display results
        print()
        print(" ".join(final[0]), file = sys.stderr)
        print(' '.join(final[1]), file = sys.stderr)
        print(' '.join(final[2]), file = sys.stderr)

if __name__ == "__main__":
    main()