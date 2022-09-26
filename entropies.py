import scipy.stats
from game_state import *


WORDS_LIST_FILE = "wordslist.txt"
ENTROPY_FILE = "entropies_final.txt"


# Preprocessing indications
INDICATIONS = list(itertools.product([Indication.GREY, Indication.YELLOW, Indication.GREEN], repeat=WORD_LEN))


class EntropyPreprocess:

    def __init__(self, words_file_path, entropy_file_path):
        # Processing words file
        words_file = open(words_file_path, "r", encoding='utf-8-sig')
        all_words = words_file.read()
        self.words_list = all_words.split("\n")
        self.num_words = len(self.words_list)
        words_file.close()

        # Processing entropy
        self.entropy_file = open(entropy_file_path, 'a')
        self.process_entropy()
        self.entropy_file.close()

    def process_entropy(self):
        count = 0
        start = False
        for word in self.words_list:
            if count % 1000 == 0:
                print("FINISHED {} words".format(count))
            if word == 'malty':
                start = True
            if start:
                entropy = self.get_entropy(word)
                to_write = word + ' ' + str(entropy) + '\n'
                print(word + ' ' + str(entropy))
                self.entropy_file.write(to_write)
            count += 1

    # Counts the number of words matching the indication according to word
    def count_possible_words(self, word, indication):
        count = 0
        for w in self.words_list:
            possible = True
            for i in range(WORD_LEN):
                if (indication[i] == Indication.GREEN and w[i] != word[i]) \
                        or (indication[i] == Indication.YELLOW and word[i] not in w) \
                        or (indication[i] == Indication.GREY and word[i] in w):
                    possible = False
            if possible:
                count += 1
        return count

    # Calculates entropy of a word according to all possible indications
    def get_entropy(self, word):
        probabilities = []
        # indications = itertools.product([Indication.GREY, Indication.YELLOW, Indication.GREEN], repeat=WORD_LEN)
        for indication in INDICATIONS:
            num_possible_words = self.count_possible_words(word, indication)
            prob = num_possible_words / self.num_words
            probabilities.append(prob)
        return scipy.stats.entropy(probabilities, base=2)


EntropyPreprocess(WORDS_LIST_FILE, ENTROPY_FILE)
