import pygame

from threading import Thread

from data import data
from main_class import MAIN

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

font = pygame.font.Font("Akzidenz-grotesk-roman.ttf",24)

opened_menu = False

class MENU:
    def __init__(self):
        self.width = 150
        self.height = 50
        self.amount_of_buttons = 3
        self.distance = 25
        self.buttons = []
        self.button_colors = [(54, 57, 63) for _ in range(self.amount_of_buttons)]
        self.text = {}

        self.setup()

    def create_menu(self):
        self.menu = pygame.draw.rect(main.window, (32, 34, 37),pygame.Rect(0,0, main.window_width, main.window_height))

        for i,v in enumerate(self.buttons):
            pygame.draw.rect(main.window, self.button_colors[i], v, 3)     
        
        for i in self.text:
            main.window.blit(font.render(i,False,(255,255,255)), (self.text[i]["x"], self.text[i]["y"]))

    def setup(self):
        self.buttons.append(pygame.Rect(self.distance,50,self.width,self.height))
        self.buttons.append(pygame.Rect(self.distance,150,self.width,self.height))
        self.buttons.append(pygame.Rect(self.distance,250,self.width,self.height))

        self.text["Save Data"] = {"x": self.distance*8, "y": 60}
        self.text["Clear Data"] = {"x": self.distance*8, "y": 160}
        self.text["Erase"] = {"x": self.distance*8, "y": 260}
         
menu = MENU()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if main.auto_save:
                data.save_data()
                
            with open("./info.txt", "w") as info:
                info_to_write = ""

                for i,v in enumerate(main.rects):
                    info_to_write += f"RECT {i+1}: x: {v.x}, y: {v.y}, width: {v.width}, height: {v.height}\n"          

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

            dragging = True
           
            if (event.pos[0] > main.current_rect.bottomright[0]-5 and event.pos[0] < main.current_rect.bottomright[0]+5) and (event.pos[1] < main.current_rect.bottomright[1]+5 and event.pos[1] > main.current_rect.bottomright[1]-5):
                
        
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

            # handling text
            if event.unicode == "t" and not listening_for_keys:
                pos = pygame.mouse.get_pos()

                if main.current_text in main.text and (pos[0] > main.current_text.x and pos[0] <= main.current_text.x+main.current_text.obj.size(main.current_text.text)[0]+5) and (pos[1] > main.current_text.y and pos[1] <= main.current_text.y+main.current_text.obj.size(main.current_text.text)[1]+5) and cond:
                    cond = True
                else:
                    cond = False

                    x = main.make_text()

                listening_for_keys = True


            elif event.key == pygame.K_RETURN and listening_for_keys:
                if cond and main.current_text:
                    cond = False

                listening_for_keys = False
                listening_for_size_change = False

            elif event.key == pygame.K_ESCAPE and not listening_for_size_change and listening_for_keys:
                listening_for_size_change = True

            elif listening_for_size_change and event.key == pygame.K_ESCAPE:
                listening_for_size_change = False

                size_to_change = ""

            elif event.key == pygame.K_BACKSPACE:
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