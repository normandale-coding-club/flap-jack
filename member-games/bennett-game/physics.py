import pygame
class physObj:
    def __init__(self, collide = True, size = 10, color = (0, 0, 0), pos = pygame.Vector2(0,0), velocity = pygame.Vector2(0,0), mass = 1):
        self.collide = collide
        self.size = size
        self.color = color
        self.pos = pos
        self.velocity = velocity
        self.mass = mass
        pass