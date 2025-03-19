import random
from game.assets import HEIGHT,WIDTH
import pygame

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255), (self.x, int(self.y)), self.size)
