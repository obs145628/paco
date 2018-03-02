'''
MDP with reinforcement learning deep mind tutorial

Only work with these features :
    Codes :
    S = Start
    G = Goal
    W = Wall
    H = Hole
    . = GROUND

Items and enemies are ignored

'''

import numpy as np
import random
from policy import Policy
from utils import clamp
import world

'''
Return the state you end up when doing a deterministic move from a state
'''
def get_next_cell(w, state, action):

    sx = int(state % w.width)
    sy = int(state / w.width)

    oldx = sx
    oldy = sy
    
    if action == world.ACTION_DOWN:
        sy += 1
    elif action == world.ACTION_LEFT:
        sx -= 1
    elif action == world.ACTION_RIGHT:
        sx += 1
    elif action == world.ACTION_UP:
        sy -= 1

    sx = clamp(sx, 0, w.width - 1)
    sy = clamp(sy, 0, w.height - 1)

    if w.get_cell(sx, sy).type == world.CELL_WALL:
        sx = oldx
        sy = oldy

    return sy * w.width + sx

'''
Compute all the states you can end up and the probabilities for each when taking action in state
'''
def get_next_states(w, state, action):

    cell = w.get_cell1(state)
    if cell.type == world.CELL_WALL or cell.type == world.CELL_GOAL or cell.type == world.CELL_HOLE:
        return ([], [])
    
    next = []
    probs = []

    for a2 in range(0, 4):
        s2 = get_next_cell(w, state, a2)

        index = len(next)
        if s2 in next:
            index = next.index(s2)
        else:
            next.append(s2)
            probs.append(0)

        p = (1 - w.proba_action_valid) / 4
        if a2 == action:
            p += w.proba_action_valid
        probs[index] += p
    
    return (next, probs)

'''
Return the reward you get in state s
'''
def get_state_reward(w, s):
    val = world.CELL_REWARDS[w.get_cell1(s).type]
    if val == None:
        val = 0
    return val   

'''
S: set of states (0 -> w.width * w.height - 1)
A: set of actions (directions 0 -> 3)
P: state transition probability matrix
R: reward function
GAMMA: discount factor
'''
class MDP:

    
    def __init__(self, w, gamma):
        self.world = w
        self.build_p()
        self.build_r()
        self.gamma = gamma


    '''
    Generate state transition probability matrix P
    P(a, s, s') = p(S_t+1 = s' | S_t = s, A_t = a) 
    '''
    def build_p(self):
        w = self.world
        P = np.zeros((4, w.width * w.height, w.width * w.height))

        for s1 in range(w.width * w.height):
            for a in range(4):
                next, probs = get_next_states(w, s1, a)
                for s2, proba in zip(next, probs):
                    P[a][s1][s2] = proba
                

        self.P = P

    '''
    Generate reward matrix R
    R(a, s) = E(R_t+1 | S_t = s, A_t = a)
    R(a, s) = sum_(s' in S) P(a, s, s') * R_t
    '''
    def build_r(self):
        w = self.world

        R = np.zeros((4, w.width * w.height))

        rewards = [0] * w.width * w.height
        for s in range(w.width * w.height):
            rewards[s] = get_state_reward(w, s)

        for a in range(4):
            for s1 in range(w.width * w.height):
                val = 0
                for s2 in range(w.width * w.height):
                    val += self.P[a][s1][s2] * rewards[s2]
                R[a][s1] = val

        self.R = R


    '''
    Return P matrx following policy
    P_pi(s, s') = sum(a in A) pi(a|s) * P(a, s, s')
    '''
    def p_policy(self, policy):

        w = self.world
        P_pi = np.zeros((w.width * w.height, w.width * w.height))

        for s1 in range(w.width * w.height):
            for s2 in range(w.width * w.height):
                val = 0
                for a in range(4):
                    val += policy.table[s1][a] * self.P[a][s1][s2]
                P_pi[s1][s2] = val

        return P_pi

    '''
    Return R table following policy
    R_pi(s) = sum(a in A) pi(a|s) * R(a, s)
    '''
    def r_policy(self, policy):

        w = self.world
        R_pi = np.zeros((w.width * w.height))
        for s in range(w.width * w.height):
            val = 0
            for a in range(4):
                val += policy.table[s][a] * self.R[a][s]
            R_pi[s] = val

        return R_pi

    ''' 
    Compute v_pi(s) solving a system of equations
    v_pi = (I - GAMMA * P_pi)^-1 * R_pi
    '''
    def policy_value_system(self, policy):
        w = self.world
        n = w.width * w.height
        m1 = np.eye(n) - self.gamma * self.p_policy(policy)
        return np.dot(np.linalg.inv(m1), self.r_policy(policy))

    '''
    Apply k steps of iterative policy evaluation
    Start with default value of 0 for each state, or another value

    v_k+1(s) = sum(a in A) pi(a|s) * (R(a, s) + GAMMA * sum(s' in S) P(a, s, s') v_k(s')) 
    v_k+1 = R_pi + GAMMA * P_pi * v_k
    Both computations are equals, second is just the matrix form
    First one is implemented
    '''
    def iterative_policy_evaluation(self, policy, k, vs = None):

        w = self.world
        n = w.width * w.height
        if vs == None:
            vs = np.zeros((n))
            
        for _ in range(k):
            new_vs = np.zeros((n))
            for s in range(n):
                val = 0
                for a in range(4):
                    val2 = 0
                    for s2 in range(n):
                        val2 += self.P[a][s][s2] * vs[s2]
                    val += policy.table[s][a] * (self.R[a][s] + self.gamma * val2)
                new_vs[s] = val
            vs = new_vs

        return vs

    '''
    Compute optimal policy from q-values
    pi(a|s) = (a == argmax(a) q(s, a) 
    '''
    def qvs_to_policy(self, qvs):

        w = self.world
        n = w.width * w.height
        policy = [0] * n

        for s in range(n):
            policy[s] = np.argmax(qvs[s])

        return Policy.build_deterministic(policy)

    ''''
    Compute q-values from values
    q(s, a) = R(a, s) + GAMMA * sum(s' in S) P(a, s, s') v(s')
    '''
    def qvs_from_vs(self, vs):
        w = self.world
        n = w.width * w.height
        qvs = np.zeros((n, 4))

        for s in range(n):
            for a in range(4):
                val = 0
                for s2 in range(n):
                    val += self.P[a, s, s2] * vs[s2]
                qvs[s][a] = self.R[a][s] + self.gamma * val

        return qvs

    
    '''
    Start with any policy pi
    1) evalute policy with iterative policy evaluation (k >= 2)
    2) choose new policy pi' that take optimal solutions from q-values
    3) if pi' is different from pi, go back to 1 with pi'
    4) policy converges, it's optimal, return it
    '''
    def policy_iteration(self, policy = None):

        w = self.world

        if policy == None:
            policy = Policy.build_deterministic([0] * w.width * w.height)

        while True:
            old_policy = policy
            vs = self.iterative_policy_evaluation(policy, 20)
            qvs = self.qvs_from_vs(vs)
            policy = self.qvs_to_policy(qvs)
            if policy == old_policy:
                break

        return policy

    '''
    Apply k steps of value iteration
    Convert to v*
    By default, start with v_0(s) = 0
    
    V_k+1(s) = max(a in A) (R(a, s) + GAMMA * sum(s' in S) P(a, s, s') * V_k(s'))
    V_k+1 = max(a in A) (R(a) + GAMMA * P(a) * V_k)
    Both computations are equal, but second one is matrix form
    '''
    def value_iteration(self, k, vs = None):
        w = self.world
        n = w.width * w.height
        if vs == None:
            vs = np.zeros((n))

        for _ in range(k):
            new_vs = np.zeros((n))

            for s in range(n):
                max_val = 0
                for a in range(4):
                    val2 = 0
                    for s2 in range(n):
                        val2 += self.P[a][s][s2] * vs[s2]

                    val = self.R[a][s] + self.gamma * val2
                    max_val = max(max_val, val)

                new_vs[s] = max_val
            
            vs = new_vs

        return vs
