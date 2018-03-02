# Paco

Paco is a basic pacman-like game in python.  
It is used to tests several artificiat intelligenge algorithms


## Setup

```
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
```

## Usage

```
cd src
python main.py <action> <algorithm> <world-file>  [options]
```

vpi: Evaluate value function of a policy for each state

- system: Solve by MPD using a system
- ipe: Iterative Policy Evaluation
- fvmc: First Visit Monte-Carlo policy evaluation
- evmc: Every Visit Monte-Carlo policy evaluation
- evmcm: Every Visit Monte-Carlo policy evaluation (with parameter alpha)
- td0: TD(0) POlicy Evaluation
- ftdl : Forward-View TD(lambda) [TODO]
- btdl : Backward-View TD(lambda) [TODO]
- offtd0: Importance sampling for Off-Policy TD(0) [TODO]

pistar: Compute the optimal policy

- piiter: Policy Iteration
- gliemc: GLIE Monte-Carlo Control
- sarsa0: SARSA for TD(0)
- fsarsal: Forward-View SARSA TD(lambda) [TODO]
- bsarsal: Backward-View SARSA TD(lambda)
- offtd0: Off-Policy learning for TD(0) [TODO]
- qlearn0: Q-Learining for TD(0)


vstar: Compute value function of optimal policy

- valiter: Value Iteration



Options:

--alpha: alpha parameter for non-stationary problems

--gui: display the window after each action

--pi: policy to be used, values:

- RAND: each move as the same probability
- UP: always up
- DOWN: always down
- LEFT: always left
- RIGHT: always right

--gamma: discount factor

--simus : Number of times to simulate games (used for Monte-Carlo and TD learning)


## Algorithm

- Reinforcement learning


## Ressources

The following tutorials have been used:

- Deep Mind RL course: <http://www0.cs.ucl.ac.uk/staff/d.silver/web/Teaching.html>
- Book Reinforcement Learning: An Introduction by Sutton and Barto: <http://incompleteideas.net/book/the-book-2nd.html>