import argparse
import numpy as np
import sys

import gaming
import mdp2
import monte_carlo
from policy import Policy
import td_learning
import world


#td learning sarsa_offline: world2

def load_policy(world, data):

    n = world.width * world.height

    if data == 'RAND':
        table = np.full((n, 4), 1. / 4.)
        return Policy(table)
    
    return None
    

def default_policy(world):
    n = world.width * world.height
    table = np.random.rand(n, 4)
    return Policy(table)

parser = argparse.ArgumentParser()
parser.add_argument('action', help='action to be realized')
parser.add_argument('algorithm', help='algorithm to do the action')
parser.add_argument('world', help='path to the world input file')
parser.add_argument('--alpha', help='parameter for non stationary problems',
                    type=float, nargs='?', default=0.5)
parser.add_argument('--gui', help='enable the gui window of the game', action='store_true')
parser.add_argument('--pi', help='policy to be used')
parser.add_argument('--gamma', help='discount factor, in [0-1], default is 1',
                    type=float, nargs='?', default=1.0)
parser.add_argument('--lbda', help='lambda parameter for TD(lambda), in [0-1], default is 0.5',
                    type=float, nargs='?', default=0.5)
parser.add_argument('--simus', help='number of times to play games, default is 10000',
                    type=int, nargs='?', default=10000)
args = parser.parse_args()

mode = args.action
algo = args.algorithm
alpha = args.alpha
gamma = args.gamma
lbda = args.lbda
nsimus = args.simus
w = world.World(args.world)
w.gui_enabled = args.gui
pi = load_policy(w, args.pi) if args.pi else default_policy(w)

if mode == 'vpi':

    if algo == 'system':
        model = mdp2.MDP(w, gamma)
        vs = model.policy_value_system(pi)
        print(vs)

    elif algo == 'ipe':
        model = mdp2.MDP(w, gamma)
        vs = model.iterative_policy_evaluation(pi, 50)
        print(vs)

    elif algo == 'fvmc':
        vs = monte_carlo.policy_evaluation_first_visit(w, pi, nsimus, gamma)
        print(vs)

    elif algo == 'evmc':
        vs = monte_carlo.policy_evaluation_every_visit(w, pi, nsimus, gamma)
        print(vs)

    elif algo == 'evmcm':
        vs = monte_carlo.policy_evaluation_update(w, pi, alpha, nsimus, gamma)
        print(vs)

    elif algo == 'td0':
        vs = td_learning.policy_evaluation_td0(w, pi, alpha, nsimus, gamma)
        print(vs)

    elif algo == 'ftdl':
        sys.stderr.write('Not implemented\n')
        sys.exit(1)

    elif algo == 'btdl':
        sys.stderr.write('Not implemented\n')
        sys.exit(1)

    elif algo == 'offtd0':
        sys.stderr.write('Not implemented\n')
        sys.exit(1)

    else:
        sys.stderr.write("Invalid algorithm: '{}'\n".format(algo))
        sys.exit(1)


elif mode == 'pistar':


    if algo == 'piiter':
        model = mdp2.MDP(w, gamma)
        pi = model.policy_iteration()
        print(pi.table)

    elif algo == 'gliemc':
        pi = monte_carlo.glie_control(w, nsimus, gamma)
        print(pi.table)

    elif algo == 'sarsa0':
        pi = td_learning.sarsa(w, alpha, nsimus, gamma)
        print(pi.table)

    elif algo == 'fsarsal':
        sys.stderr.write('Not implemented\n')
        sys.exit(1)

    elif algo == 'bsarsal':
        pi = td_learning.sarsa_lambda(w, alpha, lbda, nsimus, gamma)
        print(pi.table)

    elif algo == 'offtd0':
        sys.stderr.write('Not implemented\n')
        sys.exit(1)

    elif algo == 'qlearn0':
        pi = td_learning.sarsa_offline(w, alpha, nsimus, gamma)
        print(pi.table)
    
    else:
        sys.stderr.write("Invalid algorithm: '{}'\n".format(algo))
        sys.exit(1)


elif mode == 'vstar':


    if algo == 'valiter':
        model = mdp2.MDP(w, gamma)
        vs = model.value_iteration(50)
        print(vs)
    
    else:
        sys.stderr.write("Invalid algorithm: '{}'\n".format(algo))
        sys.exit(1)


elif mode == 'qstar':
    pass


else:
    sys.stderr.write("Invalid mode: '{}'\n".format(mode))
    sys.exit(1)


#model = mdp2.MDP(w)
#pi = model.policy_iteration()
#print(model.policy_value_system(pi))
#print(td_learning.policy_evaluation_td0(w, pi, 0.01, 100000))

#pi = monte_carlo.glie_control(w, 10000)
#pi = td_learning.sarsa(w, 0.3, 10000)


#pi = td_learning.sarsa_offline(w, 0.3, 0.1, 1000)
#pi.play_games(w, 10000)

