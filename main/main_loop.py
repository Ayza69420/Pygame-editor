import pygame
import os
import json

from time import sleep
from threading import Thread

from main.data import data
from main.main_class import MAIN

pygame.init()

clock = pygame.time.Clock()
main = MAIN()

main.setup_settings()

data = data(main)
data.get_data()

font = MAIN.font

selected = False
dragging = False

size_to_change = 24
listening_for_keys = False
listening_for_size_change = False

cond = False

taking_color_input = False
taking_font_input = False

color_button = None
color_to_change = ""

opened_menu = False
opened_settings = False

path = os.path.split(os.path.realpath(__file__))[0]

running = True

class BUTTON(pygame.Rect):
    def __init__(self, x, y, width, height, color=(54,57,63)):
        super(BUTTON, self).__init__(x, y, width, height)
        
        self.color = color

    def create(self):
        pygame.draw.rect(main.window, self.color, pygame.Rect(self.x, self.y, self.width, self.height), 3)

class TEXT:
    def __init__(self, text, x, y):
        self.text = text
        self.main = main
        self.x = x
        self.y = y
        
    def create(self):         
        self.obj = pygame.font.Font("%s/Fonts/%s" % (path, font),24).render(self.text,False,(255,255,255))

        main.window.blit(self.obj, (self.x,self.y))

class MENU:
    def __init__(self):
        self.width = 150
        self.height = 50
        self.distance = 25
        self.buttons = []
        self.text = {}

        self.setup()

    def create_menu(self):
        self.menu = pygame.draw.rect(main.window, (32, 34, 37),pygame.Rect(0,0, main.window_width, main.window_height))

        for i in self.buttons:
            i.create()
        
        for i in self.text:
            self.text[i].create()

    def setup(self):
        self.indexes = len(self.buttons)

        self.buttons.append(BUTTON(self.distance,50,self.width,self.height)) # sd
        self.buttons.append(BUTTON(self.distance,150,self.width,self.height)) # cd
        self.buttons.append(BUTTON(self.distance,250,self.width,self.height)) # e
        self.buttons.append(BUTTON(self.distance,350,self.width,self.height)) # s
        
        self.buttons.append(BUTTON(main.window_width-300, 100, 250, self.height)) # ff

        self.buttons.append(BUTTON(main.window_width-300, main.window_height-100, 50, self.height)) # r
        self.buttons.append(BUTTON(main.window_width-200, main.window_height-100, 50, self.height)) # g
        self.buttons.append(BUTTON(main.window_width-100, main.window_height-100, 50, self.height)) # b
        
        self.text["SD"] = (TEXT("Save Data", self.distance*2, 65))
        self.text["CD"] = (TEXT("Clear Data", self.distance*2, 165))
        self.text["E"] = (TEXT("Erase", self.distance*2, 265))
        self.text["S"] = (TEXT("Settings", self.distance*2, 365))
        self.text["F"] = (TEXT("Font", main.window_width-200, 25))
        self.text["C"] = (TEXT("RGB Color", main.window_width-230, main.window_height-150))

        self.text["FF"] = (TEXT("", self.buttons[self.indexes-4].x+5, self.buttons[self.indexes-4].y+15))

        # the rgb buttons are always made at the end so their indexes would be len(self.buttons) minus their order
        self.text["R"] = (TEXT(str(main.r), self.buttons[self.indexes-3].x+5, self.buttons[self.indexes-3].y+15))
        self.text["G"] = (TEXT(str(main.g), self.buttons[self.indexes-2].x+5, self.buttons[self.indexes-2].y+15))
        self.text["B"] = (TEXT(str(main.b), self.buttons[self.indexes-1].x+5, self.buttons[self.indexes-1].y+15))

class SETTINGS(MENU):
    def __init__(self):
        super(SETTINGS, self).__init__()

        self.buttons = []

        self.setup()

    def setup(self):
        self.buttons.append(BUTTON(self.distance,50,self.width,self.height))
        self.buttons.append(BUTTON(self.distance,150,self.width,self.height))

        self.text["AS"] = TEXT("Auto Save", self.distance*2, 65)
        self.text["DM"] = TEXT("Debug Mode", self.distance*1.5, 165)

menu = MENU()
settings = SETTINGS()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if main.auto_save:
                data.save_data()
                
            with open("%s/info.txt" % path, "w") as info:
                info_to_write = ""

                for i,v in enumerate(main.rects):
                    info_to_write += "RECT %s: x: %s, y: %s, width: %s, height: %s, color: %s\n" % (i+1, v.x, v.y, v.width, v.height, v.color)      

                for i,v in enumerate(main.text):
                    info_to_write += "TEXT %s: text: %s, x: %s, y: %s, text size: %s, font: %s\n" % (i+1, v.text, v.x, v.y, v.size, v.font)


                info.write(info_to_write)
            

                with open("%s/settings.json" % path, "w") as settings:
                    settings.write(json.dumps({"auto_save": main.auto_save, "debug_mode": main.debug_mode, "default_font": main.default_font}))

            pygame.quit()
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:     

            for i in main.rects:
                if i.collidepoint(event.pos):
                    main.current_rect = i

                    main.currently_interacting = "rect"
                    
            for i in main.text:
                if (event.pos[0] > i.x and event.pos[0] <= i.x+i.obj.size(i.text)[0]+5) and (event.pos[1] > i.y and event.pos[1] <= i.y+i.obj.size(i.text)[1]+5):
                    main.current_text = i

                    main.currently_interacting = "text"  

            if opened_menu:
                for i,v in enumerate(menu.buttons):
                    if v.collidepoint(event.pos):
                        if i == 0:
                            data.save_data()
                        elif i == 1:
                            data.clear_data()
                        elif i == 2:
                            main.erase()
                        elif i == 3:
                            opened_settings = True
                            opened_menu = False

            if opened_settings:
                for i,v in enumerate(settings.buttons):
                    if v.collidepoint(event.pos):
                        if i == 0:
                            if not main.auto_save:
                                main.auto_save = True
                                settings.buttons[0].color = (0,100,0)
                            elif main.auto_save:
                                main.auto_save = False
                                settings.buttons[0].color = (139,0,0)

                        elif i == 1:
                            if not main.debug_mode:
                                main.debug_mode = True
                                settings.buttons[1].color = (0,100,0)
                            elif main.debug_mode:
                                main.debug_mode = False
                                settings.buttons[1].color = (139,0,0)


            if (menu.buttons[menu.indexes-3].collidepoint(event.pos) or menu.buttons[menu.indexes-2].collidepoint(event.pos) or menu.buttons[menu.indexes-1].collidepoint(event.pos)) and not taking_font_input and opened_menu:
                taking_color_input = True

                if menu.buttons[menu.indexes-3].collidepoint(event.pos) and opened_menu:
                    color_button = menu.text["R"]
                    color_to_change = menu.text["R"].text
                if menu.buttons[menu.indexes-2].collidepoint(event.pos) and opened_menu:
                    color_button = menu.text["G"]
                    color_to_change = menu.text["G"].text
                if menu.buttons[menu.indexes-1].collidepoint(event.pos) and opened_menu:
                    color_button = menu.text["B"]
                    color_to_change = menu.text["B"].text

            if menu.buttons[menu.indexes-4].collidepoint(event.pos) and not taking_color_input and opened_menu:
                taking_font_input = True

            dragging = True
           
            if (event.pos[0] > main.current_rect.bottomright[0]-5 and event.pos[0] < main.current_rect.bottomright[0]+5) and (event.pos[1] < main.current_rect.bottomright[1]+5 and event.pos[1] > main.current_rect.bottomright[1]-5):
                
                if main.current_rect in main.rects:
                    main.redo.append({"rect_changed": main.copy_rect(main.current_rect)})

                def bottom_right():
                    try:
                        old_mouse_x = event.pos[0]
                        old_mouse_y = event.pos[1]

                        while dragging:         
                            if main.current_rect.width > main.maximum_resizing and main.current_rect.height > main.maximum_resizing:                       
                                if old_mouse_x != event.pos[0]:
                                    main.current_rect.width += (event.pos[0] - old_mouse_x)
                                    old_mouse_x = event.pos[0]

                                if old_mouse_y != event.pos[1]:
                                    main.current_rect.height += (event.pos[1] - old_mouse_y)
                                    old_mouse_y = event.pos[1]

                            sleep(0.0001)

                    except Exception as error:
                        main.debug(error)

                Thread(target=bottom_right).start()

            elif event.pos[1] <= main.current_rect.bottom and event.pos[1] > main.current_rect.bottom-5:

                if main.current_rect in main.rects:
                    main.redo.append({"rect_changed": main.copy_rect(main.current_rect)})          
                
                def height():               
                    try:     
                        old_mouse_y = event.pos[1]

                        while dragging:
                            if main.current_rect.height > main.maximum_resizing:
                                if event.pos[1] != old_mouse_y: 
                                    main.current_rect.height += event.pos[1] - old_mouse_y
                                    old_mouse_y = event.pos[1]                  
                        
                            sleep(0.0001)

                        return
                    except Exception as error:
                        main.debug(error)

                Thread(target=height).start()


            elif event.pos[0] < main.current_rect.right+5 and event.pos[0] >= main.current_rect.right-5:

                if main.current_rect in main.rects:
                    main.redo.append({"rect_changed": main.copy_rect(main.current_rect)})

                def width():
                    try:
                        old_mouse_x = event.pos[0]

                        while dragging:
                            if main.current_rect.width > main.maximum_resizing:
                                if event.pos[0] != old_mouse_x:
                                    main.current_rect.width += event.pos[0] - old_mouse_x
                                    old_mouse_x = event.pos[0]

                            sleep(0.0001)

                        return    
                    except Exception as error:
                        main.debug(error)


                Thread(target=width).start()

            else:
                if main.current_rect.collidepoint(event.pos):
                    
                    if main.current_rect in main.rects:
                        main.redo.append({"rect_changed": main.copy_rect(main.current_rect)})

                    def drag_rect():
                        old_mouse_x = event.pos[0]
                        old_mouse_y = event.pos[1]

                        try:
                            while dragging:
                                if event.pos[0] != old_mouse_x:
                                    main.current_rect.x += event.pos[0] - old_mouse_x
                                    old_mouse_x = event.pos[0]
                                if event.pos[1] != old_mouse_y:
                                    main.current_rect.y += event.pos[1] - old_mouse_y
                                    old_mouse_y = event.pos[1]

                                sleep(0.0001)

                        except Exception as error:
                            main.debug(error)

                    Thread(target=drag_rect).start()

                else:
                    if main.current_text:
                        if (event.pos[0] > main.current_text.x and event.pos[0] <= main.current_text.x+main.current_text.obj.size(main.current_text.text)[0]+5) and (event.pos[1] > main.current_text.y and event.pos[1] <= main.current_text.y+main.current_text.obj.size(main.current_text.text)[1]+5):
                            if not listening_for_keys:
                                    cond = True

                            if main.current_text in main.text:
                                main.redo.append({"text_changed": main.copy_text(main.current_text)})

                            def drag_text():


                                old_mouse_x = event.pos[0]
                                old_mouse_y = event.pos[1]

                                try:
                                    while dragging:
                                        if event.pos[0] != old_mouse_x:
                                            main.current_text.x += event.pos[0] - old_mouse_x
                                            old_mouse_x = event.pos[0]
                                        if event.pos[1] != old_mouse_y:
                                            main.current_text.y += event.pos[1] - old_mouse_y
                                            old_mouse_y = event.pos[1]

                                        sleep(0.0001)

                                except Exception as error:
                                    main.debug(error)
                                
                            Thread(target=drag_text).start()


        if event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False

        if event.type == pygame.KEYDOWN:
            if taking_color_input:
                if event.unicode.isdigit() and len(color_to_change) < 3:
                    color_to_change += event.unicode

                    color_button.text = color_to_change

                    if int(color_to_change) > 255:
                        color_to_change = ""
                        color_button.text = color_to_change

                        print("You cannot put more than a value of 255.")

            if event.unicode == "t" and not listening_for_keys and not taking_font_input:
                pos = pygame.mouse.get_pos()

                if main.current_text in main.text and (pos[0] > main.current_text.x and pos[0] <= main.current_text.x+main.current_text.obj.size(main.current_text.text)[0]+5) and (pos[1] > main.current_text.y and pos[1] <= main.current_text.y+main.current_text.obj.size(main.current_text.text)[1]+5) and cond:
                    cond = True
                else:
                    cond = False

                    x = main.make_text()

                listening_for_keys = True


            elif event.key == pygame.K_RETURN:
                if not taking_color_input and not taking_font_input:
                    if cond and main.current_text:
                        cond = False

                    listening_for_keys = False
                    listening_for_size_change = False

                elif taking_color_input:
                    taking_color_input = False

                    if not color_to_change:
                        color_to_change = "0"

                    if color_button == menu.text["R"]:
                        main.r = int(color_to_change)
                    if color_button == menu.text["G"]:
                        main.g = int(color_to_change)
                    if color_button == menu.text["B"]:
                        main.b = int(color_to_change)         

                    color_to_change = ""
                    
                elif taking_font_input:
                    taking_font_input = False

                    main.font = menu.text["FF"].text

            elif event.key == pygame.K_ESCAPE and not listening_for_size_change and listening_for_keys:
                listening_for_size_change = True

            elif listening_for_size_change and event.key == pygame.K_ESCAPE:
                listening_for_size_change = False

            elif event.unicode == "-" and listening_for_size_change:
                size_to_change -= 1

                try:
                    if cond and main.current_text:
                        main.current_text.size = size_to_change
                    else:
                        x.size = size_to_change
                except Exception as error:
                    main.debug(error)

                    print("An error occurred while trying to change the size.")

            elif event.key == pygame.K_BACKSPACE:
                if listening_for_keys:
                    if cond and main.current_text:
                        main.current_text.text = main.current_text.text[:-1]
                    else:
                        x.text = x.text[:-1]

                elif taking_color_input:
                    color_to_change = color_to_change[:-1]
                    color_button.text = color_to_change
                    
                elif taking_font_input:
                    menu.text["FF"].text = menu.text["FF"].text[:-1]

            elif event.unicode == "+" and listening_for_size_change:
                if size_to_change <= 100:
                    size_to_change += 1

                try:
                    if cond and main.current_text:
                        main.current_text.size = size_to_change
                    else:
                        x.size = size_to_change
                except Exception as error:
                    main.debug(error)

                    print("An error occurred while trying to change the size, size was reseted.")

            elif listening_for_keys and not listening_for_size_change:
                if cond and main.current_text:
                    main.current_text.text += event.unicode
                else:
                    x.text += event.unicode

            elif taking_font_input:
                menu.text["FF"].text += event.unicode
                
            ########################
            
            else:
                if not taking_color_input or not taking_font_input:
                    if event.unicode == "m":
                        if opened_menu:
                            opened_menu = False
                            taking_font_input, taking_color_input, listening_for_size_change = False, False, False
                        else:
                            opened_menu = True

                        if opened_settings:
                            opened_settings = False

                    elif event.unicode == "e":
                        main.make_rect()              

                    elif event.unicode == "r":
                        main.delete_object()

                    elif event.unicode == "z" and main.redo:
                        main.redo_action()

                    elif event.unicode == "y" and main.undo:
                        main.undo_action()

                    elif event.unicode == "c":
                        main.copy()

                    elif event.unicode == "v":
                        main.paste()

                    elif event.unicode == "x":
                        main.cut()

                    elif event.unicode == "f":
                        main.fill()

    if running:
        main.display()
        clock.tick(60)
