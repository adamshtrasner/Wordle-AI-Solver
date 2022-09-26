import math
import random

from game_state import GameState, Players, WORD_LEN
import numpy as np
import abc

US = 0
THEM = 1
THRESHOLD_EVAL_FUNC = 100

# Evaluation functions for agents
LOCAL = 'local'  # calculates state score locally, according to state's possible words (not all words)
CONST = 'const'  # returns state's constant score, calculated in advance using all words
NULL = 'null'  # random choice between all possible words of state

# Heuristic weights - chosen after testing
ENTROPY_WEIGHT = 0.6
GREEN_WEIGHT = 0.2
YELLOW_WEIGHT = 0.15
GREY_WEIGHT = 0.05

MAX_ENTROPY = 7


class Agent:
    """
    An abstract agent class. All the agents inherit from this class.
    """

    def __init__(self, depth=1, evaluation_function=None):
        self._depth = depth
        if evaluation_function == LOCAL:
            self.evaluation_function = eval_func
        elif evaluation_function == CONST:
            self.evaluation_function = eval_func_const
        else:
            self.evaluation_function = null_heuristic

    @abc.abstractmethod
    def get_action(self, state: GameState):
        return


class MinmaxAgent(Agent):
    """
    implements the MinMax Adversarial Search
    """

    def __init__(self, depth=1, evaluation_func=None):
        super().__init__(depth, evaluation_func)
        self._depth = depth
        if self._depth > 1:
            # local evaluation is not relevant with depth > 1
            self.evaluation_function = eval_func_const

    def max_value(self, state, depth):
        """
        :param state: game state object
        :param depth: depth to check
        :return: max path score
        """
        actions = state.get_legal_actions(Players.GUESSER)
        scores = self.min_max(state, actions, depth, self.min_value, Players.GUESSER)
        return max(scores)

    def min_value(self, state, depth):
        """
        :param state: game state object
        :param depth: depth to check
        :return: min path score
        """
        actions = state.get_legal_actions(Players.INDICATOR)
        scores = self.min_max(state, actions, depth, self.max_value, Players.INDICATOR)
        return min(scores)

    def min_max(self, state: GameState, actions, depth, f_val, agent):
        """
        MinMax calculation.
        :param actions: legal actions
        :param state: game state
        :param depth: current depth
        :param f_val: max or min validation
        :param agent: us VS them
        :return: score
        """
        if not actions or depth == 0:
            return [self.evaluation_function(state)]
        successors = [state.generate_successor(agent, action) for action in actions]
        if not successors:
            return [self.evaluation_function(state)]
        scores = [f_val(succ, depth - 1) for succ in successors]
        return scores

    def get_action(self, state: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and evaluation function.
        """
        set_eval_func = self.evaluation_function
        actions = state.get_legal_actions(Players.GUESSER)
        len_indications = len(state.get_possible_indications())
        if len_indications > THRESHOLD_EVAL_FUNC:
            self.evaluation_function = eval_func_const
        score_list = self.min_max(state, actions, 2 * self._depth - 1, self.min_value, Players.GUESSER)
        self.evaluation_function = set_eval_func
        return actions[np.argmax(score_list)]


class AlphaBetaAgent(Agent):
    """
    implements the AlphaBeta Adversarial Search
    """
    def __init__(self, depth=1, evaluation_func=None):
        super().__init__(depth, evaluation_func)
        self._depth = depth
        if self._depth > 1:
            # local evaluation is not relevant with depth > 1
            self.evaluation_function = eval_func_const
        self.alpha = -math.inf
        self.beta = math.inf

    def max_value(self, state, depth):
        """
        :param state: game state object
        :param depth: depth to check
        :return: max path score
        """
        actions = state.get_legal_actions(Players.GUESSER)
        scores = self.alpha_beta(state, actions, depth, self.min_value, Players.GUESSER)
        return max(scores)

    def min_value(self, state, depth):
        """
        :param state: game state object
        :param depth: depth to check
        :return: min path score
        """
        actions = state.get_legal_actions(Players.INDICATOR)
        scores = self.alpha_beta(state, actions, depth, self.max_value, Players.INDICATOR)
        return min(scores)

    def alpha_beta(self, state: GameState, actions, depth, f_val, agent):
        """
        AlphaBeta calculation.
        :param actions: legal actions
        :param state: game state
        :param depth: current depth
        :param f_val: max or min validation
        :param agent: us VS them
        :return: score
        """
        if not actions or depth == 0:
            return [self.evaluation_function(state)]
        successors = [state.generate_successor(agent, action) for action in actions]
        if not successors:
            return [self.evaluation_function(state)]

        scores = []
        if agent == Players.GUESSER:
            best_value = -math.inf
            for succ in successors:
                best_value = max(best_value, f_val(succ, depth - 1))
                self.alpha = max(self.alpha, best_value)
                if self.beta <= self.alpha:
                    break
            scores.append(best_value)
        else:
            best_value = math.inf
            for succ in successors:
                best_value = min(best_value, f_val(succ, depth - 1))
                self.alpha = min(self.alpha, best_value)
                if self.beta <= self.alpha:
                    break
            scores.append(best_value)
        return scores

    def get_action(self, state: GameState):
        """
        Returns the action after alpha-beta pruning from the current gameState
        using self.depth and evaluation function.
        """
        set_eval_func = self.evaluation_function
        actions = state.get_legal_actions(Players.GUESSER)
        len_indications = len(state.get_possible_indications())
        if len_indications > THRESHOLD_EVAL_FUNC:
            self.evaluation_function = eval_func_const
        score_list = self.alpha_beta(state, actions, 2 * self._depth - 1, self.min_value, Players.GUESSER)
        self.evaluation_function = set_eval_func
        return actions[np.argmax(score_list)]


class ExpectiMaxAgent(Agent):
    """
    implements the Expectimax Adversarial Search
    """
    def __init__(self, depth=1, evaluation_func=None):
        super().__init__(depth, evaluation_func)

    def max_value(self, state, depth):
        """
        :param state: game state object
        :param depth: depth to check
        :return: max path score
        """
        actions = state.get_legal_actions(Players.GUESSER)
        scores = self.expectimax(state, actions, depth, self.chance_value, Players.GUESSER)
        return max(scores)

    def chance_value(self, state, depth):
        """
        :param state: game state object
        :param depth: depth to check
        :return: mean of scores
        """
        actions = state.get_legal_actions(Players.INDICATOR)
        scores = self.expectimax(state, actions, depth, self.max_value, Players.INDICATOR)
        return np.mean(scores)

    def expectimax(self, state: GameState, actions, depth, f_val, agent):
        """
        Expectimax calculation.
        :param actions: legal actions
        :param state: game state
        :param depth: current depth
        :param f_val: max or min validation
        :param agent: us VS them
        :return: score
        """
        if not actions or depth == 0:
            return [self.evaluation_function(state)]
        successors = [state.generate_successor(agent, action) for action in actions]
        if not successors:
            return [self.evaluation_function(state)]
        scores = [f_val(succ, depth - 1) for succ in successors]
        return scores

    def get_action(self, state: GameState):
        """
        Returns the expectimax action from the current gameState using self.depth
        and evaluation function.
        """
        set_eval_func = self.evaluation_function
        actions = state.get_legal_actions(Players.GUESSER)
        len_indications = len(state.get_possible_indications())
        if len_indications > THRESHOLD_EVAL_FUNC:
            self.evaluation_function = eval_func_const
        score_list = self.expectimax(state, actions, 2 * self._depth - 1, self.chance_value, Players.GUESSER)
        self.evaluation_function = set_eval_func
        return actions[np.argmax(score_list)]


class DecisionTree(Agent):
    """
    implements a DecisionTree
    """
    def __init__(self, evaluation_func=None):
        super().__init__(0, evaluation_func)

    def get_action(self, state: GameState):
        """
        Returns the next decision according to the indication given in game state
        """
        actions = state.get_legal_actions(Players.GUESSER)
        if self.evaluation_function is None:
            return random.choice(actions)
        score_list = []
        for word in actions:
            new_state = GameState(word, state.words, indication=None, yellow_letters=state.get_yellow_letters(),
                             green_letters=state.get_green_letters(), possible_words=state.get_possible_words(),
                             prev_guess= state.get_prev_guess())
            score_list.append(self.evaluation_function(new_state))
        return actions[np.argmax(score_list)]

# __________________ Heuristics _______________________


def get_entropy(state: GameState):
    """
    calculates the entropy of a state, by the word it holds
    :param state: GameState object
    :return:
    """
    possible_words = state.get_possible_words()
    num_words = len(possible_words)
    entropy = 0
    if num_words == 0:
        return entropy
    indications = state.get_possible_indications()
    for indication in indications:
        sample_state = GameState(word=state.get_word(), words=state.words, indication=indication,
                                 possible_words=state.get_possible_words()[:],
                                 yellow_letters=state.get_yellow_letters().copy(),
                                 green_letters=state.get_green_letters()[:],
                                 prev_guess=state.get_prev_guess())
        sample_state.update_possible_words()
        num_possible_words = len(sample_state.get_possible_words())
        prob = num_possible_words / num_words
        if prob != 0:
            info = math.log2(1 / prob)
        else:
            info = 0
        entropy += prob * info
    return round(entropy, 5)


def get_color_avgs(word, all_words):
    """
    calculates the average number of green, yellow and grey letters of a specific word
    :param word: specified word
    :param all_words:
    :return:
    """
    if not all_words:
        return 0, 0, 0
    avg_green_letters = 0
    avg_yellow_letters = 0
    avg_grey_letters = 0
    for w in all_words:
        for i in range(WORD_LEN):
            if w[i] == word[i]:
                avg_green_letters += 1
            elif w[i] in word:
                avg_yellow_letters += 1
            elif w[i] not in word:
                avg_grey_letters += 1
    avg_green_letters /= len(all_words)
    avg_yellow_letters /= len(all_words)
    avg_grey_letters /= len(all_words)
    return avg_green_letters, avg_yellow_letters, avg_grey_letters


def eval_func(state: GameState):
    """
    evaluates scores based on possible words in the given state
    :param state: GameState object
    :return:
    """
    avg_green, avg_yellow, avg_grey = get_color_avgs( state.get_word(), state.get_possible_words())
    entropy = get_entropy(state)
    scaled_entropy = entropy / MAX_ENTROPY
    scaled_avg_green = avg_green / WORD_LEN
    scaled_avg_yellow = avg_yellow / WORD_LEN
    scaled_avg_grey = avg_grey / WORD_LEN
    return ENTROPY_WEIGHT*scaled_entropy + GREEN_WEIGHT*scaled_avg_green + \
           YELLOW_WEIGHT*scaled_avg_yellow + GREY_WEIGHT*scaled_avg_grey


def eval_func_const(state: GameState):
    """
    evaluates scores based on all words (calculations were preprocessed)
    :param state: GameState object
    :return:
    """
    word = state.get_word()
    scaled_entropy = state.words.get_entropy_scaled(word)
    scaled_avg_green = state.words.get_avg_green(word)
    scaled_avg_yellow = state.words.get_avg_yellow(word)
    scaled_avg_grey = state.words.get_avg_grey(word)
    return ENTROPY_WEIGHT*scaled_entropy + GREEN_WEIGHT*scaled_avg_green + \
           YELLOW_WEIGHT*scaled_avg_yellow + GREY_WEIGHT*scaled_avg_grey

def null_heuristic(state: GameState):
    """
    null heuristic - returns 0 for each state
    :param state:
    :return:
    """
    return 0

