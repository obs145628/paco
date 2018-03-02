import world
import numpy as np
import random

ALPHA = 0.8
GAMMA = 1

'''
Play ngames in order to evaluate a policy
sample = R(s, pi(s), s') + GAMMA * v(s')
v(s) = v(s) + ALPHA * (sample - v(s)) 
'''
def policy_evaluation(w, policy, ngames):

    vs = np.zeros(w.width * w.height)

    for _ in range(ngames):
        w.reset()
        while not w.finished:
            s = w.player.cell.pos
            a = policy[s]
            reward = w.take_action(a)
            s2 = w.player.cell.pos

            sample = reward + GAMMA * vs[s2]
            vs[s] = vs[s] + ALPHA * (sample - vs[s])

    return vs


'''
PLay ngames in order to compute the q-values
sample = R(s, a, s') + gamma * max(a') Q(s', a')
Q(s, a) = Q(s, a) + alpha * (sample - Q(s, a))

action a can be selected of different maners
tradeof between exploration and exploitation
in this case, action a is chosen randomly
'''
def q_learning(w, ngames):

    qvs = np.zeros((w.width * w.height, 4))

    for _ in range(ngames):
        w.reset()
        while not w.finished:
            s = w.player.cell.pos
            a = random.randint(0, 3)
            reward = w.take_action(a)
            s2 = w.player.cell.pos

            sample = reward + GAMMA * np.max(qvs[s2])
            qvs[s][a] = qvs[s][a] + ALPHA * (sample - qvs[s][a])
    

    return qvs
