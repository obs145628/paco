'''
Temporal difference learning methods with reinforcement learning deep mind tutorial
'''

import numpy as np
from policy import Policy

'''
Play n games in order to evaluate a policy
sample = R(s, pi(s), s') + gamma * v(s')
v(s) = v(s) + ALPHA * (sample - v(s)) 
'''
def policy_evaluation_td0(w, policy, alpha, nsimus, gamma):

    vs = np.zeros(w.width * w.height)

    for _ in range(nsimus):
        w.reset()
        while not w.finished:
            s = w.player.cell.pos
            a = policy.get_action(s)
            reward = w.take_action(a)
            s2 = w.player.cell.pos

            sample = reward + gamma * vs[s2]
            vs[s] = vs[s] + alpha * (sample - vs[s])

    return vs
'''
Play n games using SARSA (State - Action - Reward - State - Action)
Compute Q values using TD(0)
Explore following e-greedy policy
e = 1 / k, with k decresing over time
alpha : learning rate, should decrease over time 

Q(s, a) chosen arbitriraly, except Q(terminal,*) = 0
Q(s, a) = Q(s, a) + alpha * (R + gamma * Q(s', a') - Q(s, a))
'''
def sarsa(w, alpha, nsimus, gamma):

    n = w.width  * w.height
    Q = np.zeros((n, 4))

    for k in range(1, nsimus + 1):
        w.reset()
        s = w.player.cell.pos
        a = Policy.e_greedy_action_from_qvs(s, 1 / k, Q)
        
        while not w.finished:
            reward = w.take_action(a)
            s2 = w.player.cell.pos
            a2 = Policy.e_greedy_action_from_qvs(s2, 1 / k, Q)

            Q[s][a] += alpha * (reward + gamma * Q[s2][a2] - Q[s][a])

            s = s2
            a = a2

    return Policy.build_deterministic(Policy.qvs_to_table(Q))

'''
Play n games using SARSA lambda (State - Action - Reward - State - Action)
Compute Q values using TD(lambda)
Explore following e-greedy policy
e = 1 / k, with k decresing over time
alpha : learning rate, should decrease over time 

Eligibility traces E_t(s, a)
E_0(s, a) = 0
E_t(s, a) = gamma * lambda * E_t(s-1, a-1) + 1(S_t = s, A_t = a)

Q(s, a) initialized arbitriraly
err_t = R_t + gamma * Q(s_t+1, a_t+1) - Q(s_t, a_t)
Q(s, a) = Q(s, a) + alpha * err_t * E_t(s, a)
'''
def sarsa_lambda(w, alpha, lambd, nsimus, gamma):

    n = w.width  * w.height
    Q = np.zeros((n, 4))

    for k in range(1, nsimus + 1):
        w.reset()
        E = np.zeros((n, 4))
        
        s = w.player.cell.pos
        a = Policy.e_greedy_action_from_qvs(s, 1 / k, Q)
        
        while not w.finished:
            reward = w.take_action(a)
            s2 = w.player.cell.pos
            a2 = Policy.e_greedy_action_from_qvs(s2, 1 / k, Q)

            err = reward + gamma * Q[s2][a2] - Q[s][a]
            E[s][a] += 1
            
            for si in range(n):
                for ai in range(4):
                    Q[si][ai] += alpha * err * E[si][ai]
                    E[si][ai] *= gamma * lambd

            s = s2
            a = a2

    return Policy.build_deterministic(Policy.qvs_to_table(Q))


def sarsa_offline(w, alpha, nsimus, gamma):

    n = w.width  * w.height
    Q = np.zeros((n, 4))

    for t in range(1, nsimus + 1):
        w.reset()
        s = w.player.cell.pos
        epsilon = 1 / t
        
        while not w.finished:
            a = Policy.e_greedy_action_from_qvs(s, epsilon, Q)
            reward = w.take_action(a)
            s2 = w.player.cell.pos

            Q[s][a] += alpha * (reward + gamma * np.max(Q[s2]) - Q[s][a])

            s = s2

    return Policy.build_deterministic(Policy.qvs_to_table(Q))
