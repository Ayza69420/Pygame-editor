import pygame
import json
import os

from objects import RECT, TEXT
import main_loop

class MAIN:
    def __init__(self):
        self.window_height = int(input("Window height?\n"))
        self.window_width = int(input("Window width?\n"))

        try:
            assert(self.window_height >= 600 and self.window_width >= 600)
        except AssertionError:
            print("Width and height must be atleast 600.")
            exit()

        self.debug_mode = False
        self.auto_save = False
        
        self.r = 0
        self.g = 0
        self.b = 0

        self.window = pygame.display.set_mode((self.window_height, self.window_width))
        pygame.display.set_caption("Pygame editor")

        self.display_objects = [self.create_rect,self.create_text]

        self.rects = [RECT(self.window_width/2-50, self.window_height/2-50, 100, 50, self, (self.r, self.g, self.b))] 
        self.text = []

        self.maximum_resizing = 5

        self.currently_interacting = None
        self.current_rect = self.rects[0]
        self.current_text = None

        self.undo = []
        self.redo = []
        self.clipboard = None


    def display(self):
        self.window.fill((255,255,255))

        for i in self.display_objects:
            i()
        
        if main_loop.opened_menu:
            main_loop.menu.create_menu()

        pygame.display.flip()

    def create_rect(self):
        if self.rects:
            for rect in self.rects:
                rect.create()

    def create_text(self):
        if self.text:
            for text in self.text:
                text.create()

    def delete_object(self):
        x, y = pygame.mouse.get_pos()
        
        try:
            for i in self.rects:
                if i.collidepoint(x, y):
                    self.redo.append({"rect_deleted": i})

                    del self.rects[self.rects.index(i)]
                    return
            
            for i in self.text:
                if (x > i.x and x <= i.x+i.obj.size(i.text)[0]+5) and (y > i.y and y <= i.y+i.obj.size(i.text)[1]+5):
                    self.redo.append({"text_deleted": i})

                    del self.text[self.text.index(i)]
                    self.current_text = None

                    return

        except Exception as error:
            self.debug(error)

    def undo_action(self):
        try:
            action = self.undo[len(self.undo)-1]

            def del_and_append():
                self.redo.append(action)
                self.undo.pop(len(self.undo)-1)

            if "rect_deleted" in action:
                self.rects.pop(self.rects.index(action["rect_deleted"]))

                del_and_append()
            elif "text_deleted" in action:
                self.rects.pop(self.text.index(action["text_deleted"]))

                del_and_append()

            elif "rect_created" in action:
                self.rects.append(action["rect_created"])

                del_and_append()

            elif "text_created" in action:
                self.text.append(action["text_created"])

                del_and_append()

        except Exception as error:
            self.debug(error)

    def redo_action(self):
        try:
            
            action = self.redo[len(self.redo)-1]

            def del_and_append():
                self.undo.append(action)
                self.redo.pop(len(self.redo)-1)
            
            if "rect_deleted" in action:
                self.rects.append(action["rect_deleted"])

                del_and_append()
            elif "text_deleted" in action:
                self.text.append(action["text_deleted"])

                del_and_append()

            elif "rect_created" in action:
                self.rects.remove(action["rect_created"])

                del_and_append()

            elif "text_created" in action:
                self.text.remove(action["text_created"])

                del_and_append()
            
        except Exception as error:
            self.debug(error)

    def erase(self):
        self.rects = []
        self.text = []

    def copy(self):
        if self.currently_interacting == "rect":
            self.clipboard = {"rect":self.current_rect}
        elif self.currently_interacting == "text":
            self.clipboard = {"text":self.current_text}

    def paste(self):
        if "text" in self.clipboard:
            self.make_text(self.clipboard["text"].size, self.clipboard["text"].text)
        elif "rect" in self.clipboard:
            self.make_rect(self.clipboard["rect"].width, self.clipboard["rect"].height)

    def cut(self):
        self.copy()
        self.delete_object()

    def make_rect(self, width=100, height=50):
        x = RECT(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], width, height, self, (self.r, self.b, self.g))
        self.redo.append({"rect_created": x})
        self.rects.append(x) 

        return x

    def make_text(self, size=28, text=""):
        
        x = TEXT(size, text, self, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.redo.append({"text_created": x})
        self.text.append(x)

        return x

    def setup_settings(self):
        with open("settings.json", "r") as sett:
            settings = json.loads(sett.read())

            self.debug_mode = settings["debug_mode"]
            self.auto_save = settings["auto_save"]

    def debug(self, error):
        if self.debug_mode:
            with open(f"{os.path.split(os.path.realpath(__file__))[0]}\\debug.txt", "a") as debug:
                debug.write(str(error)+"\n")
