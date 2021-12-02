import pygame

class RECT(pygame.Rect):
    def __init__(self, x, y, width, height, main):
        self.main = main
        self.x = self.main.window_width/2-50
        self.y = self.main.window_height/2-50
        self.width = width
        self.height = height

    def create(self):
        self.rect = pygame.draw.rect(self.main.window, (0,0,0),pygame.Rect(self.x,self.y,self.width,self.height))

class TEXT:
    def __init__(self, size, text, main, x=25, y=25):
        self.text = text
        self.main = main
        self.x = self.main.window_width/2-50
        self.y = self.main.window_height/2-50
        self._size = size
        self.obj = pygame.font.SysFont('freesansbold.ttf',self._size)

    def create(self):     
        self.main.window.blit(self.obj.render(self.text,False,(0,0,0)), (self.x, self.y))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

        self.obj = pygame.font.SysFont('freesansbold.ttf',self._size)
