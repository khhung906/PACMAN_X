import pygame
import sys
import copy
import random
from settings import *
from player_class import *
from enemy_class import *
from AI import *


pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH//COLS
        self.cell_height = MAZE_HEIGHT//ROWS
        self.walls = []
        self.coins = []
        self.big_coins = []
        self.enemies = []
        self.fast = []
        self.e_pos = []
        self.cats = []
        self.holes = []
        self.froze = []
        self.hindrance = []
        self.p1_pos = None
        self.p2_pos = None
        self.load()
        self.player1 = Player(self, vec(self.p1_pos), vec(1, 0))
        self.player2 = Player(self, vec(self.p2_pos), vec(-1, 0))
        self.AI2 = AI(self, self.player2, self.player1)
        #self.make_enemies()
        self.time = 0

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

############################ HELPER FUNCTIONS ##################################

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

    def load(self):
        self.background = pygame.image.load('maze.png')
        # fill background with img 
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))

        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as a vector
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(xidx, yidx))
                    elif char == "c":
                        self.coins.append(vec(xidx, yidx))
                    elif char == "P":
                        self.p1_pos = [xidx, yidx]
                    elif char == "E":
                        self.p2_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.e_pos.append([xidx, yidx])
                    elif char == "B":
                        pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                                                                  self.cell_width, self.cell_height))
                    elif char == "F":
                        self.fast.append(vec(xidx, yidx))
                    elif char == "R":
                        self.cats.append(vec(xidx, yidx))
                    elif char == "H":
                        self.holes.append(vec(xidx, yidx))
                    elif char == "Z":
                        self.froze.append(vec(xidx, yidx))

        self.make_big_coins(6)

    def make_big_coins(self, numbers):
        for i in range(numbers):
            num = random.randint(0, len(self.coins)-1)
            self.big_coins.append(self.coins[num])
            self.coins.pop(num)



    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.background, GREY, (x*self.cell_width, 0),
                             (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.cell_height),
                             (WIDTH, x*self.cell_height))
        # for coin in self.coins:
        #     pygame.draw.rect(self.background, (167, 179, 34), (coin.x*self.cell_width,
        #                                                        coin.y*self.cell_height, self.cell_width, self.cell_height))

    def reset(self):
        # self.player1.lives = 3
        self.player1.current_score = 0
        self.player1.grid_pos = vec(self.player1.starting_pos)
        self.player1.pix_pos = self.player1.get_pix_pos()
        self.player1.direction *= 0

        # self.player2.lives = 3
        self.player2.current_score = 0
        self.player2.grid_pos = vec(self.player2.starting_pos)
        self.player2.pix_pos = self.player2.get_pix_pos()
        self.player2.direction *= 0
        # for enemy in self.enemies:
        #     enemy.grid_pos = vec(enemy.starting_pos)
        #     enemy.pix_pos = enemy.get_pix_pos()
        #     enemy.direction *= 0

        self.coins = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"


########################### INTRO FUNCTIONS ####################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [
                       WIDTH//2, HEIGHT//2-50], START_TEXT_SIZE, (170, 132, 58), START_FONT, centered=True)
        self.draw_text('2 PLAYERS', self.screen, [
                       WIDTH//2, HEIGHT//2+50], START_TEXT_SIZE, (44, 167, 198), START_FONT, centered=True)
        pygame.display.update()

########################### PLAYING FUNCTIONS ##################################

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player1.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player1.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player1.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player1.move(vec(0, 1))
                if event.key == pygame.K_q:
                    self.player1.set_hindrance()

        decision2 = self.AI2.decision()
        if decision2 == "TURN_LEFT":
            self.player2.move(vec(-1, 0))
        elif decision2 == "TURN_RIGHT":
            self.player2.move(vec(1, 0))
        elif decision2 == "TURN_UP":
            self.player2.move(vec(0, -1))
        elif decision2 == "TURN_DOWN":
            self.player2.move(vec(0, 1))
        # elif decision2 == "SET_HINDRANCE":
        #     self.player2.set_hindrance()


    def playing_update(self):
        self.player1.update()
        self.player2.update()
        for enemy in self.enemies:
            enemy.update()

        # for enemy in self.enemies:
        #     if enemy.grid_pos == self.player1.grid_pos:
        #         self.remove_life()

        if self.player1.status == 'froze' and self.player1.grid_pos == self.player2.grid_pos:
            self.player2.status = 'frozed'
            self.player1.status = 'normal'
            self.player1.stored_direction = None
            self.player2.stored_direction = None
        #print(self.player1.status)

        if self.player2.status == 'froze' and self.player1.grid_pos == self.player2.grid_pos:
            self.player1.status = 'frozed'
            self.player2.status = 'normal'
            self.player1.stored_direction = None
            self.player2.stored_direction = None

        self.time += 1
        if int(120-(self.time)/55) <= 0:
            self.state = "game over"

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_coins()
        self.draw_big_coins()
        self.draw_fast()
        self.draw_cat()
        self.draw_froze()
        self.draw_hindrance()
        # self.draw_grid()
        self.draw_text('PLAYER1 SCORE: {}'.format(self.player1.current_score),
                       self.screen, [60, 7], 18, WHITE, START_FONT)
        self.draw_text('{}'.format(int(120-(self.time)/55)),
                       self.screen, [WIDTH//2, 20], 18, RED, START_FONT, centered=True)
        self.draw_text('PLAYER2 SCORE: {}'.format(self.player2.current_score), self.screen, [WIDTH//2+100, 7], 18, WHITE, START_FONT)
        self.player1.draw()
        self.player2.draw()
        # for enemy in self.enemies:
        #     enemy.draw()
        pygame.display.update()

    # def remove_life(self):
    #     self.player1.lives -= 1
    #     if self.player1.lives == 0:
    #         self.state = "game over"
    #     else:
    #         self.player1.grid_pos = vec(self.player1.starting_pos)
    #         self.player1.pix_pos = self.player1.get_pix_pos()
    #         self.player1.direction *= 0
    #         # for enemy in self.enemies:
    #         #     enemy.grid_pos = vec(enemy.starting_pos)
    #         #     enemy.pix_pos = enemy.get_pix_pos()
    #         #     enemy.direction *= 0


    def draw_coins(self):
        if (int(self.time/50)%2 == 0):
            for coin in self.coins:
                pygame.draw.circle(self.screen, (124, 123, 7),
                                   (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)
    def draw_big_coins(self):
        if (int(self.time/50)%2 == 0):
            for coin in self.big_coins:
                pygame.draw.circle(self.screen, (124, 123, 7),
                                   (int(coin.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                                int(coin.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 8)

    def draw_fast(self):
        for f in self.fast:
            pygame.draw.circle(self.screen, WHITE,
                               (int(f.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                            int(f.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

    def draw_cat(self):
        for cat in self.cats:
            pygame.draw.circle(self.screen, GREY,
                               (int(cat.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                            int(cat.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

    def draw_hole(self):
        for hole in self.holes:
            pygame.draw.circle(self.screen, WHITE,
                               (int(cat.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                            int(cat.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

    def draw_hindrance(self):
        for hind in self.hindrance:
            pygame.draw.rect(self.screen, WHITE,
                               (int(hind.x*self.cell_width)+TOP_BOTTOM_BUFFER//2,
                                int(hind.y*self.cell_height)+TOP_BOTTOM_BUFFER//2, 
                                self.cell_width, self.cell_width))

    def draw_froze(self):
        for fro in self.froze:
            pygame.draw.circle(self.screen, BRIGHT_BLUE,
                               (int(fro.x*self.cell_width)+self.cell_width//2+TOP_BOTTOM_BUFFER//2,
                            int(fro.y*self.cell_height)+self.cell_height//2+TOP_BOTTOM_BUFFER//2), 5)

########################### GAME OVER FUNCTIONS ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        if self.player1.current_score > self.player2.current_score:
            self.draw_text("PLAYER1 win", self.screen, [WIDTH//2, HEIGHT//2],  52, RED, "arial", centered=True)
        elif self.player1.current_score < self.player2.current_score:
            self.draw_text("PLAYER2 win", self.screen, [WIDTH//2, HEIGHT//2],  52, RED, "arial", centered=True)
        if self.player1.current_score == self.player2.current_score:
            self.draw_text("Draw", self.screen, [WIDTH//2, HEIGHT//2],  52, RED, "arial", centered=True)
        pygame.display.update()




