from utils import clamp, manhattan_dist
import random
import gui
import fconfig



# GUI
WORLD_DX = 20
WORLD_DY = 20
CELL_SIZE = 30
CELL_COLORS = [None,
               gui.RED, #goal
               (0, 0, 75), #wall
               gui.YELLOW, #hole
               (25, 25, 25)] #ground
ITEM_IMGS = [None, None, None, None, None]
ITEM_SIZE = 20
ITEM_PATH = '../misc/item-{}.png'
AGENT_IMGS = [None, None, None, None, None, None]
AGENT_SIZE = 25
AGENT_PATH = '../misc/agent-{}.png'



CELL_GOAL = 1
CELL_WALL = 2
CELL_HOLE = 3
CELL_GROUND = 4


CELL_REWARDS = [None, 1000, None, -1000, -1]
CELL_END = [None, True, False, True, False]



class Cell:

    def __init__(self, world, x, y, type):

        self.world = world
        self.x = x
        self.y = y
        self.pos = y * world.width + x 
        self.type = type
        self.items = []
        self.agents = []

    def is_reachable(self):
        return self.type != CELL_WALL

    def get_reward(self):

        reward = 0
        finished = False

        reward += CELL_REWARDS[self.type]

        if CELL_END[self.type]:
            finished = True

        for item in self.items:
            reward += item.get_reward()
            self.world.items.remove(item)
        self.items = []

        for agent in self.agents:
            if agent.type == AGENT_PLAYER:
                continue

            if self.world.magic_pill == 0:
                reward += REWARD_KILLED
                finished = True
            else:
                reward += REWARD_KILL
                self.world.agents.remove(agent)

        if self.world.magic_pill != 0:
            self.agents = [self.world.player]


        self.world.finished = finished
        return reward

    def render(self):
        gui.fill_rect(WORLD_DX + self.x * CELL_SIZE, WORLD_DY + self.y * CELL_SIZE,
                      CELL_SIZE, CELL_SIZE,
                      CELL_COLORS[self.type]);



ITEM_APPLE = 1
ITEM_CAKE = 2
ITEM_PIZZA = 3
ITEM_MAGIC = 4
ITEM_REWARDS = [None, 1, 10, 25, 0]
ITEM_MAGIC_DURATION = 25

class Item:

    def __init__(self, world, x, y, type):

        self.cell = world.get_cell(x, y)
        self.x = x
        self.y = y
        self.type = type

    def render(self):

        x = WORLD_DX + CELL_SIZE * self.x + CELL_SIZE / 2 - ITEM_SIZE / 2
        y = WORLD_DY + CELL_SIZE * self.y + CELL_SIZE / 2 - ITEM_SIZE / 2

        if ITEM_IMGS[self.type] == None:
            ITEM_IMGS[self.type] = gui.load_img(ITEM_PATH.format(self.type),
                                                ITEM_SIZE, ITEM_SIZE)
            
        gui.draw_img(ITEM_IMGS[self.type], x, y)

    def get_reward(self):

        if self.type == ITEM_MAGIC:
            self.cell.world.magic_pill = ITEM_MAGIC_DURATION
        
        return ITEM_REWARDS[self.type]


AGENT_PLAYER = 1
AGENT_BLINKY = 2
AGENT_PINKY = 3
AGENT_INKY = 4
AGENT_CLYDE = 5
REWARD_KILL = 250
REWARD_KILLED = -500

TIMER_SCATTER = [None, None, 21, 21, 15, 15]
TIMER_CHASE = [None, None, 60, 60, 60, -1]

class Agent:

    def __init__(self, world, x, y, type):

        self.cell = world.get_cell(x, y)
        self.x = x
        self.y = y
        self.type = type
        self.is_chasing = False
        self.counter = TIMER_CHASE[self.type]
        self.last_move = None

        w = self.cell.world
        if type == AGENT_BLINKY:
            self.scatter_target = w.width - 1
        elif type == AGENT_PINKY:
            self.scatter_target = 0
        elif type == AGENT_INKY:
            self.scatter_target = w.width * w.height - 1
        elif type == AGENT_CLYDE:
            self.scatter_target = (w.height - 1) * w.width
        

    def go_to(self, x, y):
        self.x = x
        self.y = y
        self.cell.agents.remove(self)
        self.cell = self.cell.world.get_cell(x, y)
        self.cell.agents.append(self)

    def render(self):

        x = WORLD_DX + CELL_SIZE * self.x + CELL_SIZE / 2 - AGENT_SIZE / 2
        y = WORLD_DY + CELL_SIZE * self.y + CELL_SIZE / 2 - AGENT_SIZE / 2

        id = self.type
        if self.type != AGENT_PLAYER and self.cell.world.magic_pill != 0:
            id = 0

        if AGENT_IMGS[id] == None:
            AGENT_IMGS[id] = gui.load_img(AGENT_PATH.format(id),
                                                AGENT_SIZE, AGENT_SIZE)
            
        gui.draw_img(AGENT_IMGS[id], x, y)

    def make_move(self, action):

        w = self.cell.world
        sx = self.x
        sy = self.y

        oldx = sx
        oldy = sy
    
        if action == ACTION_DOWN:
            sy += 1
        elif action == ACTION_LEFT:
            sx -= 1
        elif action == ACTION_RIGHT:
            sx += 1
        elif action == ACTION_UP:
            sy -= 1

        sx = clamp(sx, 0, w.width - 1)
        sy = clamp(sy, 0, w.height - 1)

        if w.get_cell(sx, sy).type == CELL_WALL:
            sx = oldx
            sy = oldy

        self.go_to(sx, sy)
        self.last_move = action

    def is_move_change(self, action):

        w = self.cell.world
        sx = self.x
        sy = self.y

        oldx = sx
        oldy = sy
    
        if action == ACTION_DOWN:
            sy += 1
        elif action == ACTION_LEFT:
            sx -= 1
        elif action == ACTION_RIGHT:
            sx += 1
        elif action == ACTION_UP:
            sy -= 1

        sx = clamp(sx, 0, w.width - 1)
        sy = clamp(sy, 0, w.height - 1)

        if w.get_cell(sx, sy).type == CELL_WALL:
            sx = oldx
            sy = oldy

        return sx != oldx or sy != oldy

    def opposite_last(self):
        if self.last_move == ACTION_UP:
            return ACTION_DOWN
        elif self.last_move == ACTION_DOWN:
            return ACTION_UP
        elif self.last_move == ACTION_LEFT:
            return ACTION_RIGHT
        else:
            return ACTION_LEFT

    def list_possibles_moves(self):
        res = []
        opposite = self.opposite_last()
        for a in range(0, 4):
            if a != opposite and self.is_move_change(a):
                res.append(a)
        return res

    def distance_to(self, action, state):

        sx = self.x
        sy = self.y
        if action == ACTION_DOWN:
            sy += 1
        elif action == ACTION_LEFT:
            sx -= 1
        elif action == ACTION_RIGHT:
            sx += 1
        elif action == ACTION_UP:
            sy -= 1
        
        w = self.cell.world

        tx = state % w.width
        ty = state / w.width

        return manhattan_dist(sx, sy, tx, ty)
        

    '''
    Ghost AI :
    3 possible modes :
    - scatter
    - chase
    - frightened

    when in scatter or chase mode, has a target cell, in frightened mode, move randmly
   
    at each turn, the ghost must chose between all the available moves :
    moves that doesn't bang it against a wall
    can't do reverse move
    in frightened mode, it tooks a random move against these one
    otherwhise, it tooks the move that made him go closer to the target (manhatan distance)

    Change between scatter and chase with timer, specific to each ghost
    Timer pauses when in frightened mode, and go back to previous mode when frightened over

    In chase mode, the target is Pacman
    In scatter mode, each ghost have an assigned target, one of the 4 corner points
    When a ghost just changed from chase to scatter or scatter to chase, is move must be the reverse
    of the previous one
    '''
    def take_action(self):
        w = self.cell.world
        if self.type == AGENT_PLAYER:
            return

        actions = self.list_possibles_moves()

        if w.magic_pill == 0:
            if self.is_chasing:
                target = w.player.cell.pos
            else:
                target = self.scatter_target

            best_dist = 10000
            chosen_action = -1
            if self.counter == 0:
                chosen_action = self.opposite_last()
            else:
                for a in actions:
                    dist = self.distance_to(a, target)
                    if dist < best_dist:
                        best_dist = dist
                        chosen_action = a
        else:
            chosen_action = actions[random.randint(0, len(actions) - 1)]

        self.make_move(chosen_action)
                    
                


        if w.magic_pill != 0:
            return
        if self.counter == 0:
            if self.is_chasing:
                self.counter = TIMER_SCATTER[self.type]
            else:
                self.counter = TIMER_SCATTER[self.type]
            self.is_chasing = not self.is_chasing
        else:
            self.counter -= 1


ACTION_UP = 0
ACTION_DOWN = 1
ACTION_LEFT = 2
ACTION_RIGHT = 3

class World:


    '''
    Codes :
    S = Start
    G = Goal
    W = Wall
    H = Hole
    . = GROUND
    A = Apple
    C = Cake
    P = Pizza
    M = Magic
    2 = Blinky
    3 = Pinky
    4 = Inky
    5 = Clyde
    '''
    def __init__(self, path):

        conf = fconfig.FileConfig(path)

        dims = conf.get_val('MAP')
        pos = dims.index('*')
        width = int(dims[:pos].strip())
        height = int(dims[pos+1:].strip())

        desc = conf.get_desc('MAP').strip()
        lines = desc.split('\n')

        self.desc = desc
        self.width = width
        self.height = height
        self.cells = [None] * width * height
        self.items = []
        self.agents = []
        self.gui_enabled = False

        self.proba_action_valid = float(conf.get_val('proba_action_valid'))

        self.start_cell = None
        self.goal_cell = None
        self.player = None

        self.score = 0
        self.finished = False
        self.magic_pill = 0

        for y in range(0, self.height):
            for x in range(0, self.width):
                code = lines[y][x]
                if code == 'S':
                    self.set_cell(x, y, CELL_GROUND, True)
                elif code == 'G':
                    self.set_cell(x, y, CELL_GOAL)
                elif code == 'W':
                    self.set_cell(x, y, CELL_WALL)
                elif code == 'H':
                    self.set_cell(x, y, CELL_HOLE)
                elif code == '.':
                    self.set_cell(x, y, CELL_GROUND)

                elif code == 'A':
                    self.set_cell(x, y, CELL_GROUND)
                elif code == 'C':
                    self.set_cell(x, y, CELL_GROUND)
                elif code == 'P':
                    self.set_cell(x, y, CELL_GROUND)
                elif code == 'M':
                    self.set_cell(x, y, CELL_GROUND)

                elif code == '2':
                    self.set_cell(x, y, CELL_GROUND)
                elif code == '3':
                    self.set_cell(x, y, CELL_GROUND)
                elif code == '4':
                    self.set_cell(x, y, CELL_GROUND)
                elif code == '5':
                    self.set_cell(x, y, CELL_GROUND)


        gui_width = WORLD_DX + self.width * (CELL_SIZE + 2)
        gui_height = WORLD_DY + self.height * (CELL_SIZE + 2) + 50
        gui.init(gui_width, gui_height)


    def get_cell(self, x, y):
        return self.cells[y * self.width + x]

    def get_cell1(self, s):
        return self.get_cell(int(s % self.width), int(s / self.width))


    def set_cell(self, x, y, type, is_start = False):
        cell = Cell(self, x, y, type)
        self.cells[y * self.width + x] = cell
        if is_start:
            self.start_cell = cell
        if type == CELL_GOAL:
            self.goal_cell = cell

    def add_item(self, x, y, type):
        item = Item(self, x, y, type)
        self.items.append(item)
        self.get_cell(x, y).items.append(item)

    def add_agent(self, x, y, type):
        agent = Agent(self, x, y, type)
        self.agents.append(agent)
        self.get_cell(x, y).agents.append(agent)
        if type == AGENT_PLAYER:
            self.player = agent

    def reset(self):
        self.agents = []
        self.items = []

        self.score = 0
        self.finished = False
        self.magic_pill = 0

        lines = self.desc.split('\n')
        for y in range(0, self.height):
            for x in range(0, self.width):
                code = lines[y][x]
                self.get_cell(x, y).agents = []
                self.get_cell(x, y).items = []

                if code == 'A':
                    self.add_item(x, y, ITEM_APPLE)
                elif code == 'C':
                    self.add_item(x, y, ITEM_CAKE)
                elif code == 'P':
                    self.add_item(x, y, ITEM_PIZZA)
                elif code == 'M':
                    self.add_item(x, y, ITEM_MAGIC)

                elif code == '2':
                    self.add_agent(x, y, AGENT_BLINKY)
                elif code == '3':
                    self.add_agent(x, y, AGENT_PINKY)
                elif code == '4':
                    self.add_agent(x, y, AGENT_INKY)
                elif code == '5':
                    self.add_agent(x, y, AGENT_CLYDE)

        if self.gui_enabled:
            self.render()

        self.add_agent(self.start_cell.x, self.start_cell.y, AGENT_PLAYER)

    def take_action(self, action):
        reward = 0

        self.magic_pill = max(self.magic_pill - 1, 0)

        for agent in self.agents:
            agent.take_action()

        if random.random() >= self.proba_action_valid:
            action = random.randint(0, 3)

        dx = 0
        dy = 0
        if action == ACTION_DOWN:
            dy = +1
        elif action == ACTION_LEFT:
            dx = -1
        elif action == ACTION_RIGHT:
            dx = +1
        elif action == ACTION_UP:
            dy = -1

        new_x = self.player.x + dx
        new_y = self.player.y + dy

        new_x = clamp(new_x, 0, self.width - 1)
        new_y = clamp(new_y, 0, self.height - 1)

        if not self.get_cell(new_x, new_y).is_reachable():
            new_x = self.player.x
            new_y = self.player.y

        self.player.go_to(new_x, new_y)
        reward = self.player.cell.get_reward()

        if self.gui_enabled:
            self.render()


        self.score += reward
        return reward


    def render(self):

        gui.clear()

        for c in self.cells:
            c.render()
        for i in self.items:
            i.render()
        for a in self.agents:
            a.render()

        for i in range(0, self.width + 1):
            gui.draw_line(WORLD_DX + i * CELL_SIZE, WORLD_DY,
                          WORLD_DX + i * CELL_SIZE, WORLD_DY + self.height * CELL_SIZE,
                          gui.BLACK)

        for i in range(0, self.height + 1):
            gui.draw_line(WORLD_DX, WORLD_DY + i * CELL_SIZE,
                          WORLD_DX + self.width * CELL_SIZE, WORLD_DY + i * CELL_SIZE,
                          gui.BLACK)


        gui.draw_text(WORLD_DX,
                      WORLD_DY + CELL_SIZE * self.height,
                      'score: ' + str(self.score), gui.RED, 'Arial', 25)

        gui.render()
