# AI Project - Wordle
As part of our final project in the Introduction to Artificial Intelligence course, we chose to solve
the game of Wordle using the different AI methods that are specified in our report. Check it out
and Enjoy!

## Contributers 

* Adam Shtransner
* Shelly Madar
* Ofri Shtaif
* Yuval Hefets

## Instructions
- run **wordle.py -h** to see the optional arguments (agent, heuristic, depth)
- to play Wordle without AI run **wordle.py --agent Human**
- at each turn a word is entered an indication (answer) is shown
- for example: in order to see the AI play with MinMax agent, depth 1 and local evaluation, run:
**wordle.py --agent MinMax --evaluation_function local --depth 1**

## Files
- **wordle.py** - main file to run the game
- **game.py** - manages the game itself and the GUI
- **game_state.py** - has a GameState class which is in charge of keeping the game state (used word, indications...)
- **search.py** - implements all agent classes with the same API (Agent), including the heuristics
- **words.py** - manages the used words in the game (all words, frequent words) and has many getters for other files to use
- **word_data.csv** - has constant values for each word (calculated in advance), used for the const evaluation

## Comments
- we have 3 possible evaluation functions:
  - **local** - calculate score in real time, based on current possible words to guess
  - **const** - score that is calculated in advance for each word based on all 3000 frequent words
  - **null** - random choice of word out of all possible words
- frequent words
  - we chose to use the top 3000 most frequent words in english (out of all possible words), and used nltk to calculate these in advance.