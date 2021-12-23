import pygame
import os

from threading import Thread

from main.data import data
from main.main_class import MAIN

pygame.init()

main = MAIN()

main.setup_settings()

data = data(main)
data.get_data()

selected = False
dragging = False
size_to_change = ""
listening_for_keys = False
listening_for_size_change = False
cond = False
taking_color_input = False
color_button = None
color_to_change = ""

font = pygame.font.Font(f"{os.path.split(os.path.realpath(__file__))[0]}\\Akzidenz-grotesk-roman.ttf",24)

opened_menu = False

class BUTTON(pygame.Rect):
    def __init__(self, x, y, width, height):
        super(BUTTON, self).__init__(x, y, width, height)
        
        self.color = (54, 57, 63)

    def create(self):
        pygame.draw.rect(main.window, self.color, pygame.Rect(self.x, self.y, self.width, self.height), 3)

class TEXT:
    def __init__(self, text, x, y):
        self.text = text
        self.main = main
        self.x = x
        self.y = y
        
    def create(self):         
        main.window.blit(font.render(self.text,False,(255,255,255)), (self.x, self.y))

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
        self.buttons.append(BUTTON(self.distance,50,self.width,self.height))
        self.buttons.append(BUTTON(self.distance,150,self.width,self.height))
        self.buttons.append(BUTTON(self.distance,250,self.width,self.height))

        self.buttons.append(BUTTON(main.window_width-300, main.window_height-100, 50, self.height))
        self.buttons.append(BUTTON(main.window_width-200, main.window_height-100, 50, self.height))
        self.buttons.append(BUTTON(main.window_width-100, main.window_height-100, 50, self.height))

        
        self.text["SD"] = (TEXT("Save Data", self.distance*8, 70))
        self.text["CD"] = (TEXT("Clear Data", self.distance*8, 170))
        self.text["E"] = (TEXT("Erase", self.distance*8, 270))
        self.text["C"] = (TEXT("RGB Color", main.window_width-230, main.window_height-150))

        self.text["R"] = (TEXT(str(main.r), self.buttons[3].x+5, self.buttons[3].y+15))
        self.text["G"] = (TEXT(str(main.g), self.buttons[4].x+5, self.buttons[4].y+15))
        self.text["B"] = (TEXT(str(main.b), self.buttons[5].x+5, self.buttons[5].y+15))

menu = MENU()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if main.auto_save:
                data.save_data()
                
            with open(f"{os.path.split(os.path.realpath(__file__))[0]}\\info.txt", "w") as info:
                info_to_write = ""

                for i,v in enumerate(main.rects):
                    info_to_write += f"RECT {i+1}: x: {v.x}, y: {v.y}, width: {v.width}, height: {v.height}, color: {v.color}\n"          

                for i,v in enumerate(main.text):
                    info_to_write += f"TEXT {i+1}: text: {v.text}, x: {v.x}, y: {v.y}, text size: {v.size}\n"


                info.write(info_to_write)
            
            pygame.quit()
            break


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

            if menu.buttons[3].collidepoint(event.pos) or menu.buttons[4].collidepoint(event.pos) or menu.buttons[5].collidepoint(event.pos):
                taking_color_input = True

                if menu.buttons[3].collidepoint(event.pos):
                    color_button = menu.text["R"]
                if menu.buttons[4].collidepoint(event.pos):
                    color_button = menu.text["G"]
                if menu.buttons[5].collidepoint(event.pos):
                    color_button = menu.text["B"]

            dragging = True
           
            if (event.pos[0] > main.current_rect.bottomright[0]-5 and event.pos[0] < main.current_rect.bottomright[0]+5) and (event.pos[1] < main.current_rect.bottomright[1]+5 and event.pos[1] > main.current_rect.bottomright[1]-5):
                
                main.redo.append({"rect_changed": {"index": main.rects.index(main.current_rect), "object": main.copy_rect(main.current_rect)}})

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

                    except Exception as error:
                        main.debug(error)

                Thread(target=bottom_right).start()

            elif event.pos[1] <= main.current_rect.bottom and event.pos[1] > main.current_rect.bottom-5:

                main.redo.append({"rect_changed": {"index": main.rects.index(main.current_rect), "object": main.copy_rect(main.current_rect)}})          
                def height():               
                    try:     
                        old_mouse_y = event.pos[1]

                        while dragging:
                            if main.current_rect.height > main.maximum_resizing:
                                if event.pos[1] != old_mouse_y: 
                                    main.current_rect.height += event.pos[1] - old_mouse_y
                                    old_mouse_y = event.pos[1]                  
                        return
                    except Exception as error:
                        main.debug(error)

                Thread(target=height).start()


            elif event.pos[0] < main.current_rect.right+5 and event.pos[0] >= main.current_rect.right-5:

                main.redo.append({"rect_changed": {"index": main.rects.index(main.current_rect), "object": main.copy_rect(main.current_rect)}})

                def width():
                    try:
                        old_mouse_x = event.pos[0]

                        while dragging:
                            if main.current_rect.width > main.maximum_resizing:
                                if event.pos[0] != old_mouse_x:
                                    main.current_rect.width += event.pos[0] - old_mouse_x
                                    old_mouse_x = event.pos[0]

                        return    
                    except Exception as error:
                        main.debug(error)


                Thread(target=width).start()

            

            else:
                if main.current_rect.collidepoint(event.pos):

                    main.redo.append({"rect_changed": {"index": main.rects.index(main.current_rect), "object": main.copy_rect(main.current_rect)}})

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

                        except Exception as error:
                            main.debug(error)

                    Thread(target=drag_rect).start()

                else:
                    if main.current_text:
                        if (event.pos[0] > main.current_text.x and event.pos[0] <= main.current_text.x+main.current_text.obj.size(main.current_text.text)[0]+5) and (event.pos[1] > main.current_text.y and event.pos[1] <= main.current_text.y+main.current_text.obj.size(main.current_text.text)[1]+5):
                            if not listening_for_keys:
                                    cond = True

                            main.redo.append({"text_changed": main.current_text})

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

                                except Exception:
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

            if event.unicode == "t" and not listening_for_keys:
                pos = pygame.mouse.get_pos()

                if main.current_text in main.text and (pos[0] > main.current_text.x and pos[0] <= main.current_text.x+main.current_text.obj.size(main.current_text.text)[0]+5) and (pos[1] > main.current_text.y and pos[1] <= main.current_text.y+main.current_text.obj.size(main.current_text.text)[1]+5) and cond:
                    cond = True
                else:
                    cond = False

                    x = main.make_text()

                listening_for_keys = True


            elif event.key == pygame.K_RETURN:
                if not taking_color_input:
                    if cond and main.current_text:
                        cond = False

                    listening_for_keys = False
                    listening_for_size_change = False
                else:
                    taking_color_input = False

                    if color_button == menu.text["R"]:
                        main.r = int(color_button.text)
                    if color_button == menu.text["G"]:
                        main.g = int(color_button.text)
                    if color_button == menu.text["B"]:
                        main.b = int(color_button.text)         

                    color_to_change = ""
                    
            elif event.key == pygame.K_ESCAPE and not listening_for_size_change and listening_for_keys:
                listening_for_size_change = True

            elif listening_for_size_change and event.key == pygame.K_ESCAPE:
                listening_for_size_change = False

                size_to_change = ""

            elif event.key == pygame.K_BACKSPACE:
                if not taking_color_input:
                    if listening_for_size_change:
                        size_to_change = size_to_change[:-1]

                        try:
                            if cond and main.current_text:
                                main.current_text.size = int(size_to_change)
                            else:
                                x.size = int(size_to_change)
                        except Exception as error:
                            main.debug(error)

                            print("An error occurred while trying to change the size.")
                            size_to_change = ""   

                    elif listening_for_keys:
                        if cond and main.current_text:
                            main.current_text.text = main.current_text.text[:-1]
                        else:
                            x.text = x.text[:-1]
                else:
                    color_to_change = color_to_change[:-1]
                    color_button.text = color_to_change
                    
            elif listening_for_size_change:
                size_to_change += event.unicode

                try:
                    if cond and main.current_text:
                        main.current_text.size = int(size_to_change)
                    else:
                        x.size = int(size_to_change)
                except Exception as error:
                    main.debug(error)

                    print("An error occurred while trying to change the size, size was reseted.")
                    size_to_change = ""

            elif listening_for_keys and not listening_for_size_change:
                if cond and main.current_text:
                    main.current_text.text += event.unicode
                else:
                    x.text += event.unicode
                
            ########################

            elif event.unicode == "m":
                if opened_menu:
                    opened_menu = False
                else:
                    opened_menu = True

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

    main.display()
    
data.save_data()
