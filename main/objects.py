import pygame

class RECT(pygame.Rect):
    def __init__(self, x, y, width, height, main):
        self.main = main
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.index = 0

    def create(self):
        self.rect = pygame.draw.rect(self.main.window, (0,0,0),pygame.Rect(self.x,self.y,self.width,self.height))

