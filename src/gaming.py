import sys
import time
import gui
import world

def play_game_tbt(w):
    w.reset()
    w.render()
    
    while not w.finished:
        key = gui.wait_for_key()
        if key == gui.KEY_LEFT:
            w.take_action(world.ACTION_LEFT)
        elif key == gui.KEY_RIGHT:
            w.take_action(world.ACTION_RIGHT)
        elif key == gui.KEY_DOWN:
            w.take_action(world.ACTION_DOWN)
        elif key == gui.KEY_UP:
            w.take_action(world.ACTION_UP)

        elif key == gui.KEY_X:
            sys.exit(0)

        w.render()

    time.sleep(1)
    

def play_game(w):
    w.reset()
    w.render()
    move = world.ACTION_UP

    while not w.finished:
        key = gui.get_key()

        if key == gui.KEY_LEFT:
            move = world.ACTION_LEFT
        elif key == gui.KEY_RIGHT:
            move = world.ACTION_RIGHT
        elif key == gui.KEY_DOWN:
            move = world.ACTION_DOWN
        elif key == gui.KEY_UP:
            move = world.ACTION_UP
        elif key == gui.KEY_X:
            sys.exit(0)

        w.take_action(move)
        w.render()
        time.sleep(1 / 10)

    time.sleep(1)
