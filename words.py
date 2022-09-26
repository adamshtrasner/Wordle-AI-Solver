import random
import pandas as pd

# Heuristic weights - chosen after testing
ENTROPY_WEIGHT = 0.6
GREEN_WEIGHT = 0.2
YELLOW_WEIGHT = 0.15
GREY_WEIGHT = 0.05

USED_WORDS = 'used_words'
FREQ_WORDS = 'freq_words'
ALL_WORDS = 'all_words'


class Words:
    """
    Holds all used words and their constant scores
    """
    def __init__(self):
        self.word_map = pd.read_csv('word_data.csv')
        # all possible 5 letters english words
        self.all_words = self.word_file_to_list('wordslist.txt')
        # 3000 most frequent words
        self.frequent_words = self.word_file_to_list('freq_words.txt')

    def word_file_to_list(self, file_name):
        """
        converts a words file to list od words
        :param file_name:
        :return: list of words in file
        """
        words = open(file_name, 'r', encoding='utf-8-sig')
        word_lines = words.readlines()
        word_list = [word.rstrip() for word in word_lines]
        words.close()
        return word_list

    def get_word(self, word_list):
        """
        returns a random word from given word list
        :param word_list:
        :return:
        """
        if word_list == FREQ_WORDS:
            return random.choice(self.frequent_words)
        else:
            return random.choice(self.all_words)

    def _get_word_valued(self, word, value):
        """
        returnd a desired value for a word (based on pre-calculations)
        :param word: word
        :param value: desired value
        :return:
        """
        return self.word_map.loc[self.word_map['word'] == word][value].values[0]

    def get_entropy(self, word):
        """
        returns word constant entropy
        :param word:
        :return:
        """
        return self._get_word_valued(word, 'entropy')

    def get_entropy_scaled(self, word):
        """
        returns word constant scaled entropy
        :param word:
        :return:
        """
        return self._get_word_valued(word, 'entropy_scaled')

    def get_avg_green(self, word):
        """
        returns word constant scaled green letters average
        :param word:
        :return:
        """
        return self._get_word_valued(word, 'avg_green_scaled')

    def get_avg_yellow(self, word):
        """
        returns word constant scaled yellow letters average
        :param word:
        :return:
        """
        return self._get_word_valued(word, 'avg_yellow_scaled')

    def get_avg_grey(self, word):
        """
        returns word constant scaled grey letters average
        :param word:
        :return:
        """
        return self._get_word_valued(word, 'avg_grey_scaled')

    def get_word_list(self, word_list):
        """
        returns a desired word list
        :param word_list:
        :return:
        """
        if word_list == FREQ_WORDS:
            return self.frequent_words
        else:
            return self.all_words

    def get_max_value_word(self):
        """
        returns max valued word (used for starting word)
        :return:
        """
        max_word = 'which'
        max_val = 0
        for i, row in self.word_map.iterrows():
            word = row['word']
            scaled_entropy = self.get_entropy_scaled(word)
            scaled_avg_green = self.get_avg_green(word)
            scaled_avg_yellow = self.get_avg_yellow(word)
            scaled_avg_grey = self.get_avg_grey(word)
            val = ENTROPY_WEIGHT * scaled_entropy + GREEN_WEIGHT * scaled_avg_green + \
                  YELLOW_WEIGHT * scaled_avg_yellow + GREY_WEIGHT * scaled_avg_grey
            if val > max_val:
                max_val = val
                max_word = word
        return max_word