from words import *
from game import *
import time


def agents_performace_test(agent, true_words, title, results_file):
    num_guesses = 0
    num_wins = 0
    for true_word in true_words:
        game = Game()
        game.true_word = true_word
        state = GameState(START_WORD, game.words, prev_guess=set())
        while game.not_ended():
            new_guess = state.get_word()
            game.make_a_guess(new_guess)
            if not game.winning_flag:
                state.set_indication(game.indication)
                word = agent.get_action(state)
                state.set_word(word)
        num_guesses += game.guess_num
        num_wins += game.winning_flag
    results_file.write('#########################################################\n')
    results_file.write(title+'\n')
    results_file.write('AVG num guesses: ' + str(num_guesses / 3000) + '\n')
    results_file.write('TOTAL num wins: ' + str(num_wins) + '/' + str(3000)+'\n')


def performance_tests(agent):
    results = open('results.txt', 'a')
    all_words = Words().get_word_list('freq_words')
    start_time = time.time()
    if agent == 'tree':
        agents_performace_test(agent=DecisionTree(), true_words=all_words, results_file=results,
                              title='AGENT: Decision Tree, HEURISTIC: Null')
        agents_performace_test(agent=DecisionTree(evaluation_func='local'), true_words=all_words, results_file=results,
                              title='AGENT: Decision Tree, HEURISTIC: Local Evaluation')
        agents_performace_test(agent=DecisionTree(evaluation_func='const'), true_words=all_words, results_file=results,
                              title='AGENT: Decision Tree, HEURISTIC: Constant Evaluation')
        results.write('tree run time: ' + str(time.time() - start_time))
    elif agent == 'minmax':
        agents_performace_test(agent=MinmaxAgent(depth=1, evaluation_func='local'), true_words=all_words, results_file=results,
                               title='AGENT: MinMax, HEURISTIC: Local Evaluation, DEPTH: 1')
        agents_performace_test(agent=MinmaxAgent(depth=1, evaluation_func='const'), true_words=all_words, results_file=results,
                               title='AGENT: MinMax, HEURISTIC: Constant Evaluation, DEPTH: 1')
        agents_performace_test(agent=MinmaxAgent(depth=2, evaluation_func='const'), true_words=all_words, results_file=results,
                               title='AGENT: MinMax, HEURISTIC: Constant Evaluation, DEPTH: 2')
        results.write('minmax run time: ' + str(time.time() - start_time))
    elif agent == 'alphabeta':
        agents_performace_test(agent=AlphaBetaAgent(depth=1, evaluation_func='local'), true_words=all_words, results_file=results,
                               title='AGENT: AlphaBeta, HEURISTIC: Local Evaluation, DEPTH: 1')
        agents_performace_test(agent=AlphaBetaAgent(depth=1, evaluation_func='const'), true_words=all_words, results_file=results,
                               title='AGENT: AlphaBeta, HEURISTIC: Constant Evaluation, DEPTH: 1')
        agents_performace_test(agent=AlphaBetaAgent(depth=2, evaluation_func='const'), true_words=all_words, results_file=results,
                               title='AGENT: AlphaBeta, HEURISTIC: Constant Evaluation, DEPTH: 2')
        results.write('alphabeta run time: ' + str(time.time() - start_time))
    elif agent == 'expectimax':
        agents_performace_test(agent=ExpectiMaxAgent(depth=1, evaluation_func='local'), true_words=all_words, results_file=results,
                               title='AGENT: ExpectiMax, HEURISTIC: Local Evaluation, DEPTH: 1')
        agents_performace_test(agent=ExpectiMaxAgent(depth=2, evaluation_func='local'), true_words=all_words, results_file=results,
                               title='AGENT: ExpectiMax, HEURISTIC: Local Evaluation, DEPTH: 2')
        agents_performace_test(agent=ExpectiMaxAgent(depth=1, evaluation_func='const'), true_words=all_words, results_file=results,
                               title='AGENT: ExpectiMax, HEURISTIC: Constant Evaluation, DEPTH: 1')
        agents_performace_test(agent=ExpectiMaxAgent(depth=2, evaluation_func='const'), true_words=all_words, results_file=results,
                               title='AGENT: ExpectiMax, HEURISTIC: Constant Evaluation, DEPTH: 2')
        results.write('expectimax run time: ' + str(time.time() - start_time))
    results.close()


performance_tests('tree')
# performance_tests('minmax')
# performance_tests('alphabeta')
# performance_tests('expectimax')
