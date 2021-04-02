import pygame
from settings import *
import random

vec = pygame.math.Vector2

class AI:
	def __init__(self, app, me, enemy):
		self.app = app
		self.me = me
		self.enemy = enemy

	def decision(self):
		if not self.me.can_move():
			ran = random.randint(0, 10)
			if ran == 0:
				return "TURN_LEFT"
			elif ran == 1:
				return "TURN_RIGHT"
			elif ran == 2:
				return "TURN_UP"
			elif ran == 3:
				return "TURN_DOWN"
			elif ran == 4:
				return "SET_HINDRANCE"
			else:
				return "NOTHING_CHANGE"
		else:
			return "NOTHING_CHANGE"