import count_syllables
import sys
import random
import string

def load_file(file):
    try:
        with open(file) as f:
            word_lst = []
            for word in f:
                word = word.lower().strip()
                word_lst.append(word)
            return word_lst
    except OSError as e:
        print("{}\nError opening {}. Terminating program.".format(e, file),
              file=sys.stderr)
        sys.exit(1)

def main():
    dict = load_file('2of4brif.txt')
    num_word = int(input('How many words do you want to check their # of syllables? '))
    words = random.sample(dict,num_word)

    for word in words:
        try:
            num_syl = count_syllables.count_syllable(word)
            print(word, num_syl, end='\n')
        except KeyError:
            print(word + " not found", file=sys.stderr)

if __name__ == '__main__':
    main()

