import tkinter as tk
from tkinter import messagebox
from game_state import *
from search import *

COLOR_GREEN = "#53E887"
COLOR_YELLOW = "#F2E73E"
COLOR_BLACK = "#303030"
COLOR_GREY = "#8A8A8A"
COLOR_BG = "#4F4F4F"
COLOR_BUTTON = "#AAABAA"

WORD_LEN = 5
NUM_GUSSES = 6

# guess const:
G_TRUE = 0 # letter is in final location place
G_ALMOST = 1 # right letter wrong place
G_WRONG = 2 # letter not in word
G_COLORS={G_TRUE:COLOR_GREEN,
          G_ALMOST:COLOR_YELLOW,
          G_WRONG:COLOR_GREY}


WON = 1
SUCCES_TURN = 0
ERROR_WORD_LEN = -1
ERROR_GAME_OVER = -2

MSG_ERROR_LEN = f"please use a {WORD_LEN} long real word."
MSG_ERROR_GAME_OVER = "Out of guess. The word was {}"


class Game:
    """
    This class is in charge of managing the Wordle game
    """
    def __init__(self):
        self.words = Words()
        self.board = [None]*WORD_LEN  # holds the current guess.
        self.cur_mark = [None]*WORD_LEN
        self.indication = [None]*WORD_LEN
        self.green_list = [None]*WORD_LEN
        self.yellow_dict = dict()  # letter: wrong indexes
        self.bad_letters = set()  # letters with GREY indication
        self.true_word = self.words.get_word(FREQ_WORDS)
        self.legal_words = set(self.words.get_word_list(ALL_WORDS))
        self.guess_num = 0
        self.winning_flag = False

    def __legal_guess(self, word):
        """
        check if a word is legal as a guess (5 letters long and an english word)
        :param word:
        :return:
        """
        return len(word) == WORD_LEN and word in self.legal_words

    def __get_marking(self, guess):
        """
        returns an indication (answer) on a guess
        :param guess: word guessed
        """
        for i in range(len(guess)):
            if guess[i] == self.true_word[i]:
                self.cur_mark[i] = G_TRUE
                self.green_list[i] = guess[i]
                self.indication[i] = Indication.GREEN
            elif guess[i] in self.true_word:
                self.cur_mark[i] = G_ALMOST
                self.indication[i] = Indication.YELLOW
                if guess[i] not in self.yellow_dict.keys():
                    self.yellow_dict[guess[i]] = [i]
                else:
                    self.yellow_dict[guess[i]].append(i)
            else:
                self.cur_mark[i] = G_WRONG
                self.indication[i] = Indication.GREY
                self.bad_letters.add(guess[i])

    def __update_guess(self, new_guess):
        """
        updates the current guess on the board
        :param new_guess: new word guessed
        """
        self.guess_num += 1
        if new_guess == self.true_word:
            self.cur_mark = [G_TRUE]*WORD_LEN
            self.winning_flag = True
            return WON
        self.__get_marking(new_guess)
        self.board = list(new_guess)

    def make_a_guess(self, new_guess):
        """
        manages the procedure of making a new guess
        :param new_guess: new guessed word
        :return:
        """
        if self.guess_num < NUM_GUSSES:
            if self.__legal_guess(new_guess):
                return SUCCES_TURN if self.__update_guess(new_guess)!= WON else WON
            else:
                print(MSG_ERROR_LEN)
                return ERROR_WORD_LEN
        else:  # out of guesses
            print(MSG_ERROR_GAME_OVER)
            return ERROR_GAME_OVER

    def not_ended(self):
        return self.guess_num < NUM_GUSSES and not self.winning_flag


class Game_GUI:
    """
    This class handles the GUI of the Wordle game
    """
    def __init__(self):
        self.game = Game()
        self.gui = tk.Tk()
        self.agent = None
        self.state = None

        # set screen size:
        width, height = 290, 440
        self.gui.geometry("%dx%d" % (width, height))

        # set top bar:
        head = tk.Frame(self.gui, padx=5, pady=5, bg=COLOR_BLACK)
        head.pack(side="top", fill=tk.X)
        tk.Button(head, text="Exit", padx=20, pady=5, command=self.gui.quit, bg=COLOR_BUTTON).pack(side=tk.RIGHT)
        head_label = tk.Label(head, text="WORDLE", padx=20, pady=5, bg=COLOR_BLACK, fg="white")
        head_label.config(font=('Helvatical bold', 20))
        head_label.pack(side=tk.LEFT)

        # Body
        self.body = tk.Frame(self.gui, bg=COLOR_BG, padx=10, pady=5)
        self.body.pack(fill=tk.BOTH, expand = True)
        letter_size = 15
        letter_pad=5

        # guess entry
        user = tk.Frame(self.gui, padx=5, pady=5, bg=COLOR_BLACK)
        user.pack(side="bottom", fill=tk.X)
        self.input = tk.Entry(user, width=25)
        self.input.bind('<Return>', self.make_a_guess)
        but_entry = tk.Button(user, text="Enter", command=self.make_a_guess, padx=10, width=10, bg=COLOR_BUTTON)
        but_entry.grid(row=0, column=0, padx=10)
        self.input.grid(row=0, column=1, padx=10)

    def draw_line(self, word, mark, row):
        """
        sets the line of squares for new guess
        :param word: a 5 letter legal word
        :param row: row to write on ~ turn number
        """
        for i,(letter, m) in enumerate(zip(word, mark)):
            bg_color = G_COLORS[m]
            text_box = tk.Label(self.body, text=letter, width=2, height=1, padx=5, pady=5,
                                borderwidth=3, relief="solid", bg=bg_color, fg="black")
            text_box.config(font=('Helvatical bold', 20))
            text_box.grid(row=row, column=i, pady=5, padx=3)

    def make_a_guess(self, *event):
        """
        manages the procedure of making a new guess
        :param event:
        :return:
        """
        guess = self.input.get()
        self.input.delete(0, 'end')
        res = self.game.make_a_guess(guess)
        if res == SUCCES_TURN:
            self.draw_line(guess, self.game.cur_mark, self.game.guess_num)
        elif res == WON:
            self.draw_line(guess, self.game.cur_mark, self.game.guess_num)
            tk.messagebox.showinfo(title="game ended", message="you won!")
            self.gui.quit()
        elif res == ERROR_WORD_LEN:
            tk.messagebox.showwarning(title="error", message=MSG_ERROR_LEN)
        elif res == ERROR_GAME_OVER :
            tk.messagebox.showerror(title="error", message=MSG_ERROR_GAME_OVER.format(self.game.true_word))
            self.gui.quit()
        if self.game.guess_num == NUM_GUSSES:
            tk.messagebox.showerror(title="Game Over", message=MSG_ERROR_GAME_OVER.format(self.game.true_word))
            self.gui.quit()

    def __auto_run(self, guess=""):
        """
        runs the turns of the game
        :param guess:
        :return:
        """
        if not guess:
            guess = self.agent.get_action(self.state)
        self.state.set_word(guess)
        self.input.delete(0, tk.END)
        self.input.insert(0, guess)
        self.make_a_guess()
        self.state.set_indication(self.game.indication)
        self.gui.after(500, self.__auto_run)

    def run(self, agent, human_player=False):
        """
        class auto run
        :param agent:
        :param human_player:
        :return:
        """
        if not human_player:
            agent_init_guess = START_WORD
            self.agent = agent
            self.state = GameState("", self.game.words)
            self.gui.after(500, self.__auto_run, agent_init_guess)
        self.gui.mainloop()



