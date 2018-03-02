import numpy as np
import random
import world


'''
Stochastic policy
For each state, every action can be chosen with a specific probability
'''
class Policy:

    '''
    Build policy, for each state, best action as probabity 1, others have probability 0
    table: array [state] => best action
    '''
    @staticmethod
    def build_deterministic(table):

        n = len(table)
        table2 = np.zeros((n, 4))
        for s in range(n):
            table2[s][table[s]] = 1
        return Policy(table2)

    '''
    Build e-greedy policy
    m number of state
    e probability to pick a random action
    pi(a|s) = 1 - e + e/m if a is best action, e / m otherwhise 
    table: array [state] => best action
    '''
    @staticmethod
    def build_egreedy(table, e):
        n = len(table)
        table2 = np.zeros((n, 4))

        for s in range(n):
            for a in range(4):
                if table[s] == a:
                    table2[s][a] = 1 - e + (e / 4)
                else:
                    table2[s][a] = e / 4

        return Policy(table2)

    '''
    Compute policy table from q-values
    table[s] = argmax(a) q(s, a)
    table: array [state] => best action
    '''
    @staticmethod
    def qvs_to_table(qvs):
        n = qvs.shape[0]
        policy = [0] * n
        for s in range(n):
            policy[s] = np.argmax(qvs[s])
        return policy

    '''
    Return the best action in state s following q-values
    '''
    @staticmethod
    def greedy_action_from_qvs(s, qvs):
        return np.argmax(qvs[s])

    '''
    Return e-greedy action in state s following q-values
    '''
    @staticmethod
    def e_greedy_action_from_qvs(s, e, qvs):
        if random.random() > e:
            return np.argmax(qvs[s])
        else:
            return random.randint(0, 3)



        
    
    def __init__(self, table):
        self.table = table
        self.probs = None

    def compute_probs(self):
        n = len(self.table)
        self.probs = [None] * n

        for s in range(n):
            probs = [(i, self.table[s][i]) for i in range(4)]
            probs.sort(key = lambda x: - x[1])
            self.probs[s] = probs
            
    '''
    Select an action acording to the state and the stochastic policy
    '''
    def get_action(self, s):
        if self.probs == None:
            self.compute_probs()
            
        probs = self.probs[s]
        val = random.random()
        step = probs[0][1]

        i = 0
        while val > step:
            i += 1
            step += probs[i][1]

        return probs[i][0]

    '''
    Play one game following policy
    '''
    def play_game(self, w):
        w.reset()
        while not w.finished:
            s = w.player.cell.pos
            a = self.get_action(s)
            w.take_action(a)
        return w.score

    '''
    Play multiple games with policy and print states
    '''
    def play_games(self, w, nsimus):
        sum_score = 0
        min_score = float("inf")
        max_score = - float("inf")

        for _ in range(nsimus):
            score = self.play_game(w)
            sum_score += score
            min_score =min(min_score, score)
            max_score = max(max_score, score)

        print("min = " + str(min_score))
        print("av  = " + str(sum_score / nsimus))
        print("max = " + str(max_score))



    def __eq__(self, other):
        if not isinstance(other, Policy):
            raise TypeError
        else:
            return np.array_equal(self.table, other.table)
