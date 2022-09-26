from enum import Enum
import itertools
from words import *

WORD_LEN = 5
START_WORD = 'cares'  # start word of the agents - had the best constant evaluation out of all words


class Players(Enum):
    GUESSER = 0
    INDICATOR = 1


class Indication(Enum):
    GREY = 0
    YELLOW = 1
    GREEN = 2


class GameState(object):
    """
    This class handles the state of the game
    """
    def __init__(self, word, words: Words, indication=None, green_letters=None,
                 yellow_letters=None, possible_words=None, prev_guess=None):
        if possible_words is None:
            possible_words = words.get_word_list(FREQ_WORDS)
        if green_letters is None:
            green_letters = [None] * WORD_LEN
        if yellow_letters is None:
            yellow_letters = set()
        if indication is None:
            indication = [None] * WORD_LEN
        if prev_guess is None:
            prev_guess = set()
        self.words = words
        self._word = word
        self._indication = indication
        self._green_letters = green_letters
        self._yellow_letters = yellow_letters
        self._possible_words = possible_words
        self._prev_guess = prev_guess
        self._prev_possible_words_length = len(possible_words)
        self.set_indication(indication)

    def get_word(self):
        """
        returns the current word of the state
        :return:
        """
        return self._word

    def get_indication(self):
        """
        returns the current indications of the state
        :return:
        """
        return self._indication

    def get_prev_guess(self):
        """
        returns a list of the previous words guessed
        :return:
        """
        return self._prev_guess.copy()

    def get_num_of_turns(self):
        """
        returns the number of turns that took place
        :return:
        """
        return len(self._prev_guess) + 1

    def set_indication(self, indication):
        """
        sets a new indication for a word, and updates the list of possible words
        :param indication: Indication enum
        :return:
        """
        self._indication = indication
        if self._indication[0] is not None:
            self.update_possible_words()
            for i in range(WORD_LEN):
                if self._indication[i] == Indication.GREEN:
                    self.add_green_letter(self._word[i], i)
                elif self._indication[i] == Indication.YELLOW:
                    self.add_yellow_letter(self._word[i])

    def set_word(self, word):
        """
        sets a new word and updates previous guesses
        :param word:
        :return:
        """
        self._word = word
        self._indication = [None] * WORD_LEN
        self._prev_guess.add(word)

    def add_green_letter(self, letter, index):
        """
        adds a green letter to list of green letters
        :param letter:
        :param index:
        :return:
        """
        self._green_letters[index] = letter

    def add_yellow_letter(self, letter):
        """
        adds a yellow letter to the set of yellow letters
        :param letter:
        :return:
        """
        self._yellow_letters.add(letter)

    def get_green_letters(self):
        """
        returns a list of green letters
        :return:
        """
        return self._green_letters[:]

    def get_yellow_letters(self):
        """
        returns a set of the yellow letters
        :return:
        """
        return self._yellow_letters.copy()

    def get_num_green_letters(self):
        """
        returns the number of green letters so far
        :return:
        """
        return len([i for i in self._green_letters if i == Indication.GREEN])

    def get_possible_words(self):
        """
        returns a list of all possible words to guess in current state
        :return:
        """
        return self._possible_words[:]

    def get_possible_indications(self):
        """
        returns a list of all possible indications to be given in current state
        :return:
        """
        if len(self._yellow_letters) == 0 and self._green_letters == [None] * WORD_LEN:
            return list(itertools.product([Indication.GREY, Indication.YELLOW, Indication.GREEN],
                                     repeat=WORD_LEN))
        indication_map = [None]*WORD_LEN
        for i,letter in enumerate(self._word):
            if self._green_letters[i] and letter == self._green_letters[i]:
                indication_map[i] = [Indication.GREEN]
            elif letter in self._yellow_letters:
                indication_map[i] = (Indication.GREEN, Indication.YELLOW)
            else:
                indication_map[i] = (Indication.GREEN, Indication.YELLOW, Indication.GREY)
        res=[]
        for indi0 in indication_map[0]:
            for indi1 in indication_map[1]:
                for indi2 in indication_map[2]:
                    for indi3 in indication_map[3]:
                        for indi4 in indication_map[4]:
                            res.append([indi0, indi1, indi2, indi3, indi4])
        return res

    def update_possible_words(self):
        """
        updates the list of possible words
        :return:
        """
        possible_words = []
        for w in self._possible_words:
            possible = True
            for i in range(WORD_LEN):
                if (self._indication[i] == Indication.GREEN and w[i] != self._word[i]) \
                        or (
                        self._indication[i] == Indication.YELLOW and (self._word[i] not in w or w[i] == self._word[i])) \
                        or (self._indication[i] == Indication.GREY and self._word[i] in w):
                    possible = False
                    break
            if possible and w not in self._prev_guess:
                possible_words.append(w)
        self._prev_possible_words_length = len(self._possible_words)
        self._possible_words = possible_words

    def get_legal_actions(self, agent):
        """
        returns the legal actions of a player
        :param agent:
        :return:
        """
        if agent == Players.INDICATOR:
            return self.get_possible_indications()
        elif agent == Players.GUESSER:
            return self._possible_words
        else:
            raise Exception("illegal agent index.")

    def generate_successor(self, agent, action):
        """
        generates a successor for an action
        :param agent:
        :param action: word or indication
        :return:
        """
        yellow_letters = self._yellow_letters.copy()
        green_letters = self._green_letters[:]
        possible_words = self._possible_words[:]
        if agent == Players.INDICATOR:
            return GameState(self.get_word(), self.words, indication=action, yellow_letters=yellow_letters,
                             green_letters=green_letters, possible_words=possible_words,
                             prev_guess= self.get_prev_guess())
        elif agent == Players.GUESSER:
            return GameState(action, self.words, yellow_letters=yellow_letters,
                             green_letters=green_letters, possible_words=possible_words,
                             prev_guess= self.get_prev_guess())
        else:
            raise Exception("illegal agent index.")
