from pygame.math import Vector2 as vec

# screen settings
# 2x original 
WIDTH, HEIGHT = 732, 804
FPS = 60
TOP_BOTTOM_BUFFER = 60
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER

ROWS = 30
COLS = 28

# colour settings
BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
BRIGHT_BLUE = (0,78,255)
PLAYER_COLOUR = (190, 194, 15)

# font settings
START_TEXT_SIZE = 16
START_FONT = 'arial black'

# player settings
# PLAYER_START_POS = vec(2, 2)

# mob settings
