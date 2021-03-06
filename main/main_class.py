import pygame
import json
import os

from datetime import datetime
from main.objects import RECT, TEXT

import main.main_loop as main_loop

class MAIN:
    with open("%s/debug.txt" % os.path.split(os.path.realpath(__file__))[0], "w") as deb:
        deb.write("")
        
    with open("%s/settings.json" % os.path.split(os.path.realpath(__file__))[0], "r") as sett:
        font = json.loads(sett.read())["default_font"]

    # making sure the font exists in the folder, otherwise we use the default font

    directory = os.listdir("%s/Fonts" % os.path.split(os.path.realpath(__file__))[0])

    if font not in directory:
        with open("%s/settings.json" % os.path.split(os.path.realpath(__file__))[0]), "r" as sett:
            default_font = json.loads(sett.read())["default_font"]
            
            if default_font not in directory:
                print("Change the default font in the settings.json file with an installed font in the fonts folder.")
            else:
                font = default_font
    
    def __init__(self):
        self.window_height = int(input("Window height?\n"))
        self.window_width = int(input("Window width?\n"))

        self.debug_mode = False
        self.auto_save = False
        self.auto_update = False

        self.default_settings = {"auto_save": False, "debug_mode": True, "auto_update": False, "default_font": "Akzidenz-grotesk-roman.ttf"}

        self.path = os.path.split(os.path.realpath(__file__))[0]

        self.window_color = (255,255,255)
        
        self.r = 0
        self.g = 0
        self.b = 0

        self.window = pygame.display.set_mode((self.window_height, self.window_width))
        pygame.display.set_caption("Pygame editor")

        self.window_width, self.window_height = self.window.get_width(), self.window.get_height()

        self.display_objects = [self.create_rect,self.create_text]

        self.rects = [RECT(self.window_width/2-50, self.window_height/2-50, 100, 50, self, (self.r, self.g, self.b))] 
        self.text = []

        self.maximum_resizing = 10

        self.currently_interacting = None
        self.current_rect = self.rects[0]
        self.current_text = None

        self.undo = []
        self.redo = []
        self.clipboard = {}


    def display(self):
        self.window.fill(self.window_color)

        main_loop.settings.buttons[0].color = ((139,0,0), (0,100,0))[self.auto_save]
        main_loop.settings.buttons[1].color = ((139,0,0), (0,100,0))[self.debug_mode]
        main_loop.settings.buttons[2].color = ((139,0,0), (0,100,0))[self.auto_update]

        for i in self.display_objects:
            i()
        
        if main_loop.opened_menu:
            main_loop.menu.create_menu()

        if main_loop.opened_settings:
            main_loop.settings.create_menu()

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
                self.undo.pop()

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

            elif "rect_changed" in action:
                rect = action["rect_changed"]

                for i,v in enumerate(self.rects):
                    if v.id == rect.id:
                        self.redo.append({"rect_changed": self.copy_rect(v)})

                        self.rects.pop(i)
                        self.rects.append(rect)

                        self.undo.pop()

            elif "text_changed" in action:
                text = action["text_changed"]

                for i,v in enumerate(self.text):
                    if v.id == text.id:
                        self.redo.append({"text_changed": self.copy_text(v)})

                        self.text.pop(i)
                        self.text.append(text)

                        self.undo.pop()

            elif "rect_color" in action:
                rect = action["rect_color"]

                for i,v in enumerate(self.rects):
                    if v.id == rect.id:
                        self.redo.append({"rect_color": self.copy_rect(v)})

                        self.rects[i].color = rect.color
                        self.undo.pop()

            elif "text_color" in action:
                text = action["text_color"]

                for i,v in enumerate(self.text):
                    if v.id == text.id:
                        self.redo.append({"text_color": self.copy_text(v)})

                        self.text[i].color = text.color
                        self.undo.pop()

            elif "background_color" in action:
                color = action["background_color"]

                self.redo.append({"background_color": self.window_color})
                self.window_color = (color[0], color[1], color[2])

                self.undo.pop()

        except Exception as error:
            self.debug(error)

    def redo_action(self):
        try:
            
            action = self.redo[len(self.redo)-1]

            def del_and_append():
                self.undo.append(action)
                self.redo.pop()
            
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

            elif "rect_changed" in action:
                rect = action["rect_changed"]

                for i,v in enumerate(self.rects):
                    if v.id == rect.id:
                        self.undo.append({"rect_changed": self.copy_rect(v)})

                        self.rects.pop(i)
                        self.rects.append(rect)

                        self.redo.pop()

            elif "text_changed" in action:                
                text = action["text_changed"]

                for i,v in enumerate(self.text):
                    if v.id == text.id:
                        self.undo.append({"text_changed": self.copy_text(v)})

                        self.text.pop(i)
                        self.text.append(text)

                        self.redo.pop()

            elif "rect_color" in action:
                rect = action["rect_color"]

                for i,v in enumerate(self.rects):
                    if v.id == rect.id:
                        self.undo.append({"rect_color": self.copy_rect(v)})

                        self.rects[i].color = rect.color
                        self.redo.pop()

            elif "text_color" in action:
                text = action["text_color"]

                for i,v in enumerate(self.text):
                    if v.id == text.id:
                        self.undo.append({"text_color": self.copy_text(v)})

                        self.text[i].color = text.color
                        self.redo.pop()

            elif "background_color" in action:
                color = action["background_color"]

                self.undo.append({"background_color": self.window_color})
                self.window_color = (color[0], color[1], color[2])

                self.redo.pop()

        except Exception as error:
            self.debug(error)

    def erase(self):
        self.rects = []
        self.text = []

    def copy(self):
        x, y = pygame.mouse.get_pos()
        
        try:
            for i in self.text:
                if (x > i.x and x <= i.x+i.obj.size(i.text)[0]+5) and (y > i.y and y <= i.y+i.obj.size(i.text)[1]+5):
                    self.clipboard = {"text": i}

                    return
                
            for i in self.rects:
                if i.collidepoint(x, y):
                    self.clipboard = {"rect": i}

                    return
        except Exception as error:
            self.debug(error)

    def paste(self):
        if "text" in self.clipboard:
            obj = self.clipboard["text"]
            text = TEXT(obj.size, obj.text, self, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], obj.font, obj.color)

            self.text.append(text)
            self.redo.append({"text_created": text})

        elif "rect" in self.clipboard:
            obj = self.clipboard["rect"]
            rect = RECT(pygame.mouse.get_pos()[0]-(obj.width//2), pygame.mouse.get_pos()[1]-(obj.height//2), obj.width, obj.height, self, obj.color)
            
            self.rects.append(rect)
            self.redo.append({"rect_created": rect})

    def cut(self):
        self.copy()
        self.delete_object()

    def make_rect(self, width=100, height=50):
        x = RECT(pygame.mouse.get_pos()[0]-(width//2), pygame.mouse.get_pos()[1]-(height//2), width, height, self, (self.r, self.b, self.g))
        self.redo.append({"rect_created": x})
        self.rects.append(x) 

        return x

    def make_text(self, size=28, text=""):      
        x = TEXT(size, text, self, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],  "%s/Fonts/%s" % (os.path.split(os.path.realpath(__file__))[0], self.font, [self.r, self.g, self.b]))

        self.redo.append({"text_created": x})
        self.text.append(x)

        return x

    def setup_settings(self):
        settings = "%s/settings.json" % self.path

        with open(settings, "r") as sett:
            settings = None

            try:
                settings = json.loads(sett.read())
            except:
                with open(settings, "w") as sett:
                    sett.write(json.dumps(self.default_settings))

                settings = json.loads(sett.read())

            self.debug_mode = settings["debug_mode"]
            self.auto_save = settings["auto_save"]
            self.default_font = settings["default_font"]
            self.auto_update = settings["auto_update"]

    def debug(self, error):
        if self.debug_mode:
            with open("%s/debug.txt" % self.path, "a") as debug:
                debug.write("%s %s | %s\n" % (datetime.date(datetime.now()),datetime.time(datetime.now()),str(error)))
                
    def copy_rect(self, obj):
        return RECT(obj.x, obj.y, obj.width, obj.height, self, obj.color, obj.id)

    def copy_text(self, obj):
        return TEXT(obj.size, obj.text, self, obj.x, obj.y, obj.font, obj.color, obj.id)

    def fill(self):
        x,y = pygame.mouse.get_pos()
    
        for i in self.rects:
            if i.collidepoint((x,y)):
                self.redo.append({"rect_color": self.copy_rect(i)})

                i.color = (self.r, self.g, self.b)

                return
        
        for i in self.text:
            if (x > i.x and x <= i.x+i.obj.size(i.text)[0]+5) and (y > i.y and y <= i.y+i.obj.size(i.text)[1]+5):
                self.redo.append({"text_color": self.copy_text(i)})
                
                i.color = (self.r, self.g, self.b)

                return
            
        if not main_loop.opened_menu and not main_loop.opened_settings:
            self.redo.append({"background_color": self.window_color})

            self.window_color = (self.r, self.g, self.b)
