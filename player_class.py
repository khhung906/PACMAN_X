import pygame
from settings import *
import time
import random
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos, ini_d):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos(self.grid_pos)
        self.direction = ini_d
        self.stored_direction = None
        self.able_to_move = True
        self.status = 'normal'
        self.current_score = 0
        self.speed = 2
        self.lives = 1
        self.angry_pic = pygame.transform.scale(pygame.image.load('pic/angry_face.png'), (self.app.cell_width, self.app.cell_width))
        self.frozed_pic = pygame.transform.scale(pygame.image.load('pic/frozed_face.png'), (self.app.cell_width, self.app.cell_width))
        self.qq_pic = pygame.transform.scale(pygame.image.load('pic/QQ_face.png'), (self.app.cell_width, self.app.cell_width))
        self.scared_pic = pygame.transform.scale(pygame.image.load('pic/scared_face.png'), (self.app.cell_width, self.app.cell_width))
        self.money_pic = pygame.transform.scale(pygame.image.load('pic/money_face.png'), (self.app.cell_width, self.app.cell_width))
        self.tom_pic = pygame.transform.scale(pygame.image.load('pic/Tom_head.png'), (self.app.cell_width, self.app.cell_width))
        self.tom_pic_big = pygame.transform.scale(self.tom_pic, (HEIGHT//2, WIDTH//2))
        self.tom_pic_small = pygame.transform.scale(self.tom_pic, (self.app.cell_width, self.app.cell_width))
        self.cats_pic = [pygame.image.load(f'pic/nyan-cat{i}.png') for i in range(4)]
        self.cats_pic_count = 0
        self.cats_pic_pos = -500
        self.was_on_hole = False
        self.hindrance_item = 5
        self.frozed_time = 0


    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction*self.speed
            self.was_on_hole = False
        if self.time_to_move():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER +
                            self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER +
                            self.app.cell_height//2)//self.app.cell_height+1
        if self.on_coin():
            self.eat_coin()

        if self.on_big_coin():
            self.eat_big_coin()

        if self.on_fast():
            self.eat_fast()
            time.sleep(1)

        if self.on_cat():
            self.eat_cat()

        if self.on_froze():
            self.eat_froze()

        if self.on_hole() and not self.was_on_hole:
            self.was_on_hole = True
            self.random_move()
            self.direction = vec(0, 0)

        if self.status == 'normal':
            self.speed = 2

        elif self.status == 'speedy':
            self.speed = 4

        elif self.status == 'froze':
            self.speed = 3

        elif self.status == 'frozed':
            self.frozed_time += 1
            if self.frozed_time >= 1000:
                self.frozed_time = 0
                self.status = 'normal'

    def draw(self):
        if self.status == 'normal':
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (int(self.pix_pos.x),
                                                                int(self.pix_pos.y)), self.app.cell_width//2-2)
            #self.app.screen.blit(self.qq_pic, (int(self.pix_pos.x)-self.app.cell_width/2, int(self.pix_pos.y)-self.app.cell_width/2))

        elif self.status == 'speedy':
            # pygame.draw.circle(self.app.screen, RED, (int(self.pix_pos.x),
            #                                         int(self.pix_pos.y)), self.app.cell_width//2-2)
            self.app.screen.blit(self.tom_pic_small, (int(self.pix_pos.x)-self.app.cell_width/2, int(self.pix_pos.y)-self.app.cell_width/2))

        elif self.status == 'catty':
            # pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (int(self.pix_pos.x),
            #                                                     int(self.pix_pos.y)), self.app.cell_width//2-2)
            self.app.screen.blit(self.money_pic, (int(self.pix_pos.x)-self.app.cell_width/2, int(self.pix_pos.y)-self.app.cell_width/2))
            self.app.screen.blit(self.cats_pic[int(self.cats_pic_count)], (self.cats_pic_pos, 0))
            self.cats_pic_count = ((self.cats_pic_count+0.2))%4
            self.cats_pic_pos += 3
            if self.cats_pic_pos >= 750:
                self.status = 'normal'

        elif self.status == 'froze':
            pygame.draw.circle(self.app.screen, BRIGHT_BLUE, (int(self.pix_pos.x),
                                                                int(self.pix_pos.y)), self.app.cell_width//2-2)

        elif self.status == 'frozed':
            self.app.screen.blit(self.frozed_pic, (int(self.pix_pos.x)-self.app.cell_width/2, int(self.pix_pos.y)-self.app.cell_width/2))
        # Drawing the grid pos rect
        # pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
        #                                         self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def on_big_coin(self):
        if self.grid_pos in self.app.big_coins:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_big_coin(self):
        self.app.big_coins.remove(self.grid_pos)
        self.current_score += 3

    def on_fast(self):
        if self.grid_pos in self.app.fast:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_fast(self):
        # self.app.screen.blit(self.tom_pic_big, (HEIGHT//2-self.tom_pic_big.get_height()//2, WIDTH//2-self.tom_pic_big.get_width()//2))
        pygame.display.update()
        self.app.fast.remove(self.grid_pos)
        self.status = 'speedy'

    def on_cat(self):
        if self.grid_pos in self.app.cats:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_cat(self):
        self.app.cats.remove(self.grid_pos)
        self.status = 'catty'

    def on_froze(self):
        if self.grid_pos in self.app.froze:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_froze(self):
        self.app.froze.remove(self.grid_pos)
        self.status = 'froze'

    def on_hole(self):
        if self.grid_pos in self.app.holes:
            if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def random_move(self):
        random_num = random.randint(0, 3)
        self.pix_pos = self.get_pix_pos(self.app.holes[random_num])

    def move(self, direction):
        self.stored_direction = direction

    def set_hindrance(self):
        if(self.grid_pos-self.direction) not in self.app.walls and self.hindrance_item >= 1:
            self.app.hindrance.append(self.grid_pos-self.direction)
            self.hindrance_item -= 1

    def get_pix_pos(self, g_pos):
        return vec((g_pos[0]*self.app.cell_width)+TOP_BOTTOM_BUFFER//2+self.app.cell_width//2,
                   (g_pos[1]*self.app.cell_height) +
                   TOP_BOTTOM_BUFFER//2+self.app.cell_height//2)

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos+self.direction) == wall:
                return False
        for hind in self.app.hindrance:
            if vec(self.grid_pos+self.direction) == hind:
                return False
        if self.status == 'frozed':
            return False
        return True








