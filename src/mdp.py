'''
MDP with cs_xxx
'''

from utils import clamp, argmax
import world

'''
Only work with these features :
    Codes :
    S = Start
    G = Goal
    W = Wall
    H = Hole
    . = GROUND

Items and enemies are ignored
'''


#Learning decay
GAMMA = 1


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
Compute the value of a particular state using value iteration

v_k+1 (s) = max_(a) sum(s') (T(s, a, s') * (R(s, a, s') + gamma * v_k(s')))
'''
def get_state_value(w, vs, state):

    cell = w.get_cell1(state)

    if cell.type == world.CELL_GOAL:
        return 0
    
    if cell.type == world.CELL_WALL:
        return 0

    if cell.type == world.CELL_HOLE:
        return 0

    max_val = -1000000

    for action in range(0, 4):

        next, probs = get_next_states(w, state, action)
        val = 0
        for s2, p in zip(next, probs):
            val += p * (world.CELL_REWARDS[w.get_cell1(s2).type] + GAMMA * vs[s2])
        max_val = max(max_val, val)

    return max_val


'''
Compute one iteration of the value iteration algorithm
'''
def value_iter_rec(w, vs):
    next_vs = [0] * w.width * w.height
    for s in range(0, w.width * w.height):
        next_vs[s] = get_state_value(w, vs, s)
    return next_vs

'''
Compute k iterations of the value iteration algorithm
'''
def value_iter(w, k):
    vs = [0] * w.width * w.height
    for _ in range(0, k):
        vs = value_iter_rec(w, vs)
    return vs



'''
Compute the value of a particular state using value iteration, with fixed policy

v_k+1 (s) = max_(a) sum(s') (T(s, a, s') * (R(s, a, s') + gamma * v_k(s')))
'''
def get_policy_state_value(w, vs, state, policy):

    cell = w.get_cell1(state)

    if cell.type == world.CELL_GOAL:
        return 0
    
    if cell.type == world.CELL_WALL:
        return 0

    if cell.type == world.CELL_HOLE:
        return 0

    action = policy[state]
    next, probs = get_next_states(w, state, action)
    val = 0
    for s2, p in zip(next, probs):
        val += p * (world.CELL_REWARDS[w.get_cell1(s2).type] + GAMMA * vs[s2])

    return val

'''
Compute one iteration of the value iteration algorithm with fixed policy
'''
def policy_value_iter_rec(w, vs, policy):
    next_vs = [0] * w.width * w.height
    for s in range(0, w.width * w.height):
        next_vs[s] = get_policy_state_value(w, vs, s, policy)
    return next_vs

'''
Compute k iterations of the value iteration algorithm with fixed policy
'''
def policy_value_iter(w, k, policy):
    vs = [0] * w.width * w.height
    for _ in range(0, k):
        vs = policy_value_iter_rec(w, vs, policy)
    return vs


'''
Compute the best action of a particular state using one step value iteration

pi* (s) = arg_max_(a) sum(s') (T(s, a, s') * (R(s, a, s') + gamma * v_k(s')))
'''
def get_state_action(w, vs, state):

    cell = w.get_cell1(state)

    if cell.type == world.CELL_GOAL:
        return None
    
    if cell.type == world.CELL_WALL:
        return None

    if cell.type == world.CELL_HOLE:
        return None

    max_val = -1000000
    max_action = None

    for action in range(0, 4):

        next, probs = get_next_states(w, state, action)
        val = 0
        for s2, p in zip(next, probs):
            val += p * (world.CELL_REWARDS[w.get_cell1(s2).type] + GAMMA * vs[s2])
        if val > max_val:
            max_val = val
            max_action = action

    return max_action


'''
Use policy extraction to find policy from v*
Return array : [state] => action
'''
def policy_extraction(w, vs):

    policy = [None] * w.width * w.height
    
    for s in range(0, w.width * w.height):
        policy[s] = get_state_action(w, vs, s)

    return policy

'''
Use policy extraction to find policy from q*
Return array : [state] => action
'''
def policy_extraction_q(w, qvs):

    policy = [None] * w.width * w.height
    for s in range(0, w.width * w.height):
        policy[s] = argmax(qvs[s])
    return policy

def policy_equals(p1, p2):
    for i in range(len(p1)):
        if p1[i] != p2[i]:
            return False
    return True

'''
Apply policy iteration :
1) start width any policy
2) use value iteration to find values of policy
3) improve policy with policy extraction
4) go to 2 until the policy converges
'''
def policy_iteration(w):

    policy = [world.ACTION_UP] * w.width * w.height

    while True:

        vs = policy_value_iter(w, 20, policy)
        policy2 = policy_extraction(w, vs)

        if policy_equals(policy, policy2):
            break
        
        policy = policy2

    return policy    

'''
Play a game using policy in table: [state] => action
'''
def play_game_policy(w, policy):
    w.reset()
    while not w.finished:
        s = w.player.cell.pos
        a = policy[s]
        w.take_action(a)
    return w.score

'''
Play multiple games with policy and print states
'''
def play_games_policy(w, policy, nsimus):
    sum_score = 0
    min_score = float("inf")
    max_score = - float("inf")

    for _ in range(nsimus):
       score = play_game_policy(w, policy)
       sum_score += score
       min_score =min(min_score, score)
       max_score = max(max_score, score)

    print("min = " + str(min_score))
    print("av  = " + str(sum_score / nsimus))
    print("max = " + str(max_score))
    

'''
Use policy extraction to find optimal policy then play it on several games
'''
def simu_policy_extraction(w, nsimus):
    vs = value_iter(w, 20)
    policy = policy_extraction(w, vs)
    play_games_policy(w, policy, nsimus)
    
'''
Use policy iteration to find optimal policy then play it on several games
'''
def simu_policy_iteration(w, nsimus):
    policy = policy_iteration(w)
    play_games_policy(w, policy, nsimus)





'''
Compute the Q-value of a particular state and action using q-value iteration
q_k+1 (s, a) = sum(s') T(s, a, s') (R(s, a, s') + gamma * max(a') q_k(s', a'))
'''
def get_state_action_qvalue(w, qvs, state, action):

    cell = w.get_cell1(state)

    if cell.type == world.CELL_GOAL:
        return 0
    
    if cell.type == world.CELL_WALL:
        return 0

    if cell.type == world.CELL_HOLE:
        return 0

    qval = 0
    next, probs = get_next_states(w, state, action)

    for s2, p in zip(next, probs):
        qval += p * (world.CELL_REWARDS[w.get_cell1(s2).type] + GAMMA * max(qvs[s2]))

    return qval



'''
Compute one iteration of the q-value iteration algorithm
'''
def qvalue_iter_rec(w, qvs):
    next_qvs = [[0 for _ in range(4)] for _ in range(w.width * w.height)]
    for s in range(0, w.width * w.height):
        for a in range(0, 4):
            next_qvs[s][a] = get_state_action_qvalue(w, qvs, s, a)
    return next_qvs

'''
Compute k iterations of the q-value iteration algorithm
'''
def qvalue_iter(w, k):
    qvs = [[0 for _ in range(4)] for _ in range(w.width * w.height)]
    for _ in range(0, k):
        qvs = qvalue_iter_rec(w, qvs)
    return qvs

'''
Use qvalue iteration to find optimal policy then play it on several games
'''
def simu_qvalue_iter(w, nsimus):
    qvs = qvalue_iter(w, 20)
    policy = policy_extraction_q(w, qvs)
    play_games_policy(w, policy, nsimus)
