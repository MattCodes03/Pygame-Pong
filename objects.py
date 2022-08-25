import pygame
import random


class Paddel:
    VEL = 10

    def __init__(self, x, y, width, height, colour, score):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.score = score

    def draw(self, window):
        pygame.draw.rect(window, self.colour,
                         (self.x, self.y, self.width, self.height))

    def move(self, direction=1):
        self.y = self.y + self.VEL * direction

    def get_point(self):
        self.score += 1


class AI(Paddel):
    def __init__(self, x, y, width, height, colour, score):
        super().__init__(x, y, width, height, colour, score)

    def move(self, y):
        self.y = y


class Ball:
    VEL = 5

    def __init__(self, x, y, radius, colour):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.x_vel = self.VEL
        self.y_vel = 0
        self.MAX_VEL = self.VEL

    def draw(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y), self.radius)

    def reset(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
