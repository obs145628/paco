import pygame

_width = 800
_height = 600
_ready = False
_screen = None

def _prepare():

    global _ready
    global _screen

    if not _ready:
        _ready = True

        pygame.init()
        _screen = pygame.display.set_mode((_width, _height))


def _get_font(name, size):
    _prepare()
    font = pygame.font.SysFont(name, size)
    return font


COLOR_AMBER = (255, 191, 0)
COLOR_AQUA = (0, 255, 255)
COLOR_BOLE = (121, 68, 59)
COLOR_BROWN = (150, 75, 0)
COLOR_CYAN = (0, 183, 235)
COLOR_DARK_BLUE = (0, 0, 139)
COLOR_DARK_GRAY = (169, 169, 169)
COLOR_EMERALD = (80, 200, 120)
COLOR_FUCHSIA = (255, 0, 255)
COLOR_GOLD = (212, 175, 55)
COLOR_GRAY = (128, 128, 128)
COLOR_GREEN = (0, 255, 0)
COLOR_INDIGO = (0, 65, 106)
COLOR_JADE = (0, 168, 107)
COLOR_LEMON = (255, 247, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)


KEY_UP = pygame.K_UP
KEY_DOWN = pygame.K_DOWN
KEY_RIGHT = pygame.K_RIGHT
KEY_LEFT = pygame.K_LEFT
KEY_X = pygame.K_x

def init(width, height):

    global _width
    global _height

    _width = width
    _height = height

def clear():
    _prepare()
    _screen.fill(BLACK)

def render():
    _prepare()
    pygame.display.flip()

def wait_for_quit():
    _prepare()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT: break

def draw_line(x1, y1, x2, y2, color, width = 1):
    _prepare()
    pygame.draw.line(_screen, color, (x1, y1), (x2, y2), width)

def fill_rect(x, y, w, h, color):
    _prepare()
    pygame.draw.rect(_screen, color, (x, y, w, h), 0)

def fill_circle(x, y, r, color):
    _prepare()
    pygame.draw.circle(_screen, color, (int(x), int(y)), int(r), 0)

def draw_text(x, y, text, color, font, size):
    _prepare()
    font = _get_font(font, size)
    _screen.blit(font.render(text, True, color), (x, y))

def load_img(path, width = None, height = None):
    img = pygame.image.load(path)
    if width != None:
        img = pygame.transform.scale(img, (width, height))
    return img

def draw_img(img, x, y):
    _screen.blit(img, (x, y))

def get_event():
    evt = pygame.event.poll()
    if evt.type == pygame.NOEVENT:
        return None
    return evt

def get_key():
    while True:
        evt = pygame.event.poll()
        if evt.type == pygame.NOEVENT:
            return None
        if evt.type == pygame.KEYDOWN:
            return evt.key

def wait_for_key():
    _prepare()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN: return event.key
