import pygame

pygame.init()

class RECT(pygame.Rect):
    def __init__(self, x, y, width, height, main, color):
        super(RECT, self).__init__(x, y, width, height)

        self.main = main
        self.color = color

    def create(self):
        self.rect = pygame.draw.rect(self.main.window, (self.color),pygame.Rect(self.x,self.y,self.width,self.height))
        
class TEXT:
    def __init__(self, size, text, main, x, y):
        self.text = text
        self.main = main
        self.x = x
        self.y = y
        self._size = size
        self.obj = pygame.font.SysFont("freesansbold.ttf",self._size)

    def create(self):         
        self.main.window.blit(self.obj.render(self.text,False,(0,0,0)), (self.x, self.y))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if self._size <= 100:
            self._size = size

            self.obj = pygame.font.SysFont("freesansbold.ttf",self._size)
        else:
            print("Size cannot be greater than 100.")
