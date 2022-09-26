import argparse
from game import *

START_WORD = 'cares'

# Different Agents
HUMAN = 'Human'
DECISION_TREE = 'DecisionTree'
MINMAX = 'MinMax'
ALPHABETA = 'AlphaBeta'
EXPECTIMAX = 'Expectimax'


def main():
    """
    runs the game with given parameters
    :return:
    """
    parser = argparse.ArgumentParser(description='Wordle AI Game')
    agents = [HUMAN, DECISION_TREE, MINMAX, ALPHABETA, EXPECTIMAX]
    heuristics = [CONST, LOCAL, NULL]
    parser.add_argument('--agent', choices=agents, help='The agent (AI model or human player)', default=HUMAN, type=str)
    parser.add_argument('--depth', help='The maximum depth for to search in the game tree.', default=0, type=int)
    parser.add_argument('--evaluation_function', choices=heuristics, help='The evaluation function for the AI agents - local, const or null',
                        default='null', type=str)
    args = parser.parse_args()
    human_player = False
    depth = args.depth
    heuristic = None if args.evaluation_function == 'null' else args.evaluation_function
    if args.agent == HUMAN:
        human_player = True
        agent = None
    elif args.agent == MINMAX:
        agent = MinmaxAgent(depth=depth, evaluation_func=heuristic)
    elif args.agent == ALPHABETA:
        agent = AlphaBetaAgent(depth=depth, evaluation_func=heuristic)
    elif args.agent == EXPECTIMAX:
        agent = ExpectiMaxAgent(depth=depth, evaluation_func=heuristic)
    else:
        agent = DecisionTree(evaluation_func=heuristic)
    gui = Game_GUI()
    gui.run(agent, human_player=human_player)


if __name__ == '__main__':
    main()
