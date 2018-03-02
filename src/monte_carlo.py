'''
Monte carlo methods with reinforcement learning deep mind tutorial
'''

import numpy as np
from policy import Policy

'''
Compute an approximation of v_pi by running lots of simulations following policy pi
N(s) = 0
S(s) = 0

first time t that state s is visited:
  N(s) += 1
  S(s) += G_t

V_pi(s) = S(s) / N(s)
'''
def policy_evaluation_first_visit(w, policy, nsimus, gamma):

    n = w.width * w.height

    N = np.zeros((n))
    S = np.zeros((n))

    for _ in range(nsimus):

        #array of tuple (gamma^n (current discount), total reward)
        #one for each state, since first visit
        returns = [None] * n

        w.reset()

        while not w.finished:
            s = w.player.cell.pos
            a = policy.get_action(s)
            reward = w.take_action(a)

            if returns[s] == None:
                returns[s] = (1, 0)

            for i in range(n):
                if returns[i] != None:
                    returns[i] = (returns[i][0] * gamma, returns[i][1] + returns[i][0] * reward)

        for s in range(n):
            if returns[s] != None:
                N[s] += 1
                S[s] += returns[s][1]

    vs = np.zeros((n))
    for s in range(n):
        if N[s] != 0:
            vs[s] = S[s] / N[s]
    return vs
    

'''
Compute an approximation of v_pi by running lots of simulations following policy pi
N(s) = 0
S(s) = 0

every time t that state s is visited:
  N(s) += 1
  S(s) += G_t

V_pi(s) = S(s) / N(s)
'''
def policy_evaluation_every_visit(w, policy, nsimus, gamma):

    n = w.width * w.height

    N = np.zeros((n))
    S = np.zeros((n))

    for _ in range(nsimus):

        #array of tuple (gamma^n (current discount), total reward, start step)
        #one entry for each time step
        returns = []

        w.reset()

        while not w.finished:
            s = w.player.cell.pos
            a = policy.get_action(s)
            reward = w.take_action(a)

            returns.append((1, 0, s))
            for t in range(len(returns)):
                returns[t] = (returns[t][0] * gamma, returns[t][1] + returns[t][0] * reward, returns[t][2])

        
        for t in range(len(returns)):
            s = returns[t][2]
            N[s] += 1
            S[s] += returns[t][1]

    vs = np.zeros((n))
    for s in range(n):
        if N[s] != 0:
            vs[s] = S[s] / N[s]
    return vs


'''
Compute an approximation of v_pi by running lots of simulations following policy pi
alpha: learning rate

after each simulation, for each time step t:
  v_pi(S_t) = v_pi(S_t) + alpha * (G_t -v_pi(S_t))

'''
def policy_evaluation_update(w, policy, alpha, nsimus, gamma):

    n = w.width * w.height
    vs = np.zeros((n))

    for _ in range(nsimus):

        #array of tuple (gamma^n (current discount), total reward, start step)
        #one entry for each time step
        returns = []

        w.reset()

        while not w.finished:
            s = w.player.cell.pos
            a = policy.get_action(s)
            reward = w.take_action(a)

            returns.append((1, 0, s))
            for t in range(len(returns)):
                returns[t] = (returns[t][0] * gamma, returns[t][1] + returns[t][0] * reward, returns[t][2])

        
        for t in range(len(returns)):
            s_t = returns[t][2]
            g_t = returns[t][1] 
            vs[s_t] += alpha * (g_t - vs[s_t])


    return vs


'''
Implement monte carlo control with GLIE policy
Evaluate Q actions from each episode k with monte carlo
Compute e-greedy policy after each episode k with e = 1/k
Converges to optimal policy
'''
def glie_control(w, nsimus, gamma, policy = None):

    n = w.width * w.height
    N = np.zeros((n, 4))
    Q = np.zeros((n, 4))
    if policy == None:
        policy = Policy.build_deterministic([0] * n)

    for k in range(1, nsimus + 1):

        #array of tuple (gamma^n (current discount), total reward, start step, start action)
        #one entry for each time step
        returns = []

        w.reset()

        while not w.finished:
            s = w.player.cell.pos
            a = policy.get_action(s)
            reward = w.take_action(a)

            returns.append((1, 0, s, a))
            for t in range(len(returns)):
                returns[t] = (returns[t][0] * gamma, returns[t][1] + returns[t][0] * reward, returns[t][2], returns[t][3])

        for t in range(len(returns)):
            s_t = returns[t][2]
            g_t = returns[t][1]
            a_t = returns[t][3]
            N[s_t][a_t] += 1
            Q[s_t][a_t] += (g_t - Q[s_t][a_t]) / N[s_t][a_t]

        policy = Policy.build_egreedy(Policy.qvs_to_table(Q), 1 / k)


    return Policy.build_deterministic(policy.qvs_to_table(Q))
