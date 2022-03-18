import pygame
import os
import json

ids = []
path = os.path.split(os.path.realpath(__file__))[0]

def create_id():
    ID = len(ids)+1

    ids.append(ID)
    
    return ID

pygame.init()

class RECT(pygame.Rect):
    def __init__(self, x, y, width, height, main, color, ID=None):
        super(RECT, self).__init__(x, y, width, height)

        if ID == None:
            self.id = create_id()
        else:
            self.id = ID

        self.main = main
        self.color = color

    def create(self):
        self.rect = pygame.draw.rect(self.main.window, (self.color),pygame.Rect(self.x,self.y,self.width,self.height))
        
class TEXT:
    def __init__(self, size, text, main, x, y, font, color=(0,0,0), ID=None):
        if ID == None:
            self.id = create_id()
        else:
            self.id = ID

        self.text = text
        self.main = main
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self._size = size

        try:
            self.obj = pygame.font.Font(font,self._size)
        except FileNotFoundError:
            with open(path+"\\settings.json") as settings:
                font = json.loads(settings.read())["default_font"]

                self.font = f"{path}\\Fonts\\{font}"
                self.obj = pygame.font.Font(self.font, self._size)

                print("Invalid font.")

    def create(self):         
        self.main.window.blit(self.obj.render(self.text,False,self.color), (self.x, self.y))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if self._size <= 100:
            self._size = size

            self.obj = pygame.font.Font(self.font,self._size)
        else:
            print("Size cannot be greater than 100.")
