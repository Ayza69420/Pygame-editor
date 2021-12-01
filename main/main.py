import pygame
from threading import Thread

from data import data
from objects import RECT, TEXT

pygame.init()

class MAIN:
    def __init__(self):
        self.window_height = int(input('Window height?\n'))
        self.window_width = int(input('Window width?\n'))

        try:
            assert(self.window_height >= 600 and self.window_width >= 600)
        except AssertionError:
            print('Width and height must be atleast 600.')
            exit()

        self.window = pygame.display.set_mode((self.window_height, self.window_width))
        self.clock = pygame.time.Clock()

        self.currently_interacting = None
        self.current_rect = RECT(self.window_width/2-50, self.window_height/2-50, 100, 50, self)
        self.current_text = None

        self.rects = [self.current_rect] 
        self.text = []


    def display(self):
        self.window.fill((255,255,255))

        self.create_rect()
        self.create_text()
        self.render_text()

        pygame.display.update()
        self.clock.tick(60)

    def render_text(self):
        font = pygame.font.SysFont('freesansbold.ttf',32)
        text = font.render(f'Position: ({self.current_rect.x},{self.current_rect.y}) | Size:  (Width: {self.current_rect.width} | Height: {self.current_rect.height})',False,(0,0,0))

        if self.currently_interacting == 'rect':
            text = font.render(f'Position: ({self.current_rect.x},{self.current_rect.y}) | Size:  (Width: {self.current_rect.width} | Height: {self.current_rect.height})',False,(0,0,0))
        elif self.currently_interacting == 'text':
            size = self.current_text.obj.size(self.current_text.text)
            w = size[0]
            h = size[1]
            
            text = font.render(f'Position: ({self.current_text.x},{self.current_text.y}) | Size:  (Width: {w} | Height: {h})',False,(0,0,0))

        self.window.blit(text, (10, self.window_height-25))

    def create_rect(self):
        if self.rects:
            for rect in self.rects:
                rect.create()

    def create_text(self):
        if self.text:
            for text in self.text:
                text.create()

               


main = MAIN()
data = data(main)

data.get_data()

selected = False
dragging = False
text_to_add = ""
size_to_change = ""
listening_for_keys = False
listening_for_size_change = False

print("""
| HOTKEYS  
|
| S = Save Data
| C = Clear Data	    
| E = Create New Rect
| R = Remove Rect
| T = Create text (This won't create text if your mouse is on an existing text, instead edit it)
|
| TEXT CONTROL HOTKEYS
|
| Backspace = Removes text
| Enter = Finish/End
| Escape (esc) = Change text size 
| Escape (esc) again = Finish/End Changing
""")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        if event.type == pygame.MOUSEBUTTONDOWN:
            
            for i in main.rects:
                if i.collidepoint(event.pos):
                    main.current_rect = i

                    main.currently_interacting = 'button'
                    
            for i in main.text:
                if (event.pos[0] > i.x and event.pos[0] <= i.x+i.obj.size(i.text)[0]+5) and (event.pos[1] > i.y and event.pos[1] <= i.y+i.obj.size(i.text)[1]+5):
                    main.current_text = i

                    main.currently_interacting = 'text'


            dragging = True
           
            if (event.pos[0] > main.current_rect.bottomright[0]-5 and event.pos[0] < main.current_rect.bottomright[0]+5) and (event.pos[1] < main.current_rect.bottomright[1]+5 and event.pos[1] > main.current_rect.bottomright[1]-5):
                
                def bottom_right():
                    try:
                        old_mouse_x = event.pos[0]
                        old_mouse_y = event.pos[1]

                        while dragging:
                            if old_mouse_x != event.pos[0]:
                                main.current_rect.width += (event.pos[0] - old_mouse_x)
                                old_mouse_x = event.pos[0]

                            if old_mouse_y != event.pos[1]:
                                main.current_rect.height += (event.pos[1] - old_mouse_y)
                                old_mouse_y = event.pos[1]

                            if main.current_rect.height < 20:
                                main.current_rect.height = 20
                            if main.current_rect.width < 20:
                                main.current_rect.width = 20
                    except Exception:
                        pass

                Thread(target=bottom_right).start()

            elif event.pos[1] <= main.current_rect.bottom and event.pos[1] > main.current_rect.bottom-5:
                
                def height():               
                    try:     
                        old_mouse_y = event.pos[1]

                        while dragging:
                            main.current_rect.height += event.pos[1] - old_mouse_y
                            old_mouse_y = event.pos[1]

                            if main.current_rect.height < 20:
                                main.current_rect.height = 20
                        return
                    except Exception:
                        pass

                Thread(target=height).start()


            elif event.pos[0] < main.current_rect.right+5 and event.pos[0] >= main.current_rect.right-5:

                def width():
                    try:
                        old_mouse_x = event.pos[0]

                        while dragging:
                            main.current_rect.width += event.pos[0] - old_mouse_x
                            old_mouse_x = event.pos[0]

                            if main.current_rect.width < 20:
                                main.current_rect.width = 20
                        return    
                    except Exception:
                        pass


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
                        except Exception:
                            pass

                    Thread(target=drag_rect).start()

                else:    
                    try:
                        if (event.pos[0] > main.current_text.x and event.pos[0] <= main.current_text.x+main.current_text.obj.size(main.current_text.text)[0]+5) and (event.pos[1] > main.current_text.y and event.pos[1] <= main.current_text.y+main.current_text.obj.size(main.current_text.text)[1]+5):
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
                                    pass
                                
                            Thread(target=drag_text).start()
                    except Exception:
                        pass


        if event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False

        if event.type == pygame.KEYDOWN:

            # handling text

            def cond_check():
                pos = pygame.mouse.get_pos()

                try:
                    if (pos[0] > main.current_text.x and pos[0] <= main.current_text.x+main.current_text.obj.size(main.current_text.text)[0]+5) and (pos[1] > main.current_text.y and pos[1] <= main.current_text.y+main.current_text.obj.size(main.current_text.text)[1]+5):
                        return True
                    return False
                except Exception:
                    pass

            if event.unicode == 't' and not listening_for_keys:
                if cond_check():
                    text_to_add = main.current_text.text       
                else:
                    x = TEXT(24, text_to_add, main)
                    x.index = len(main.text)
                    main.text.append(x)

                listening_for_keys = True

            elif event.key == pygame.K_RETURN:
                if cond_check():
                    main.current_text.text = text_to_add
                else:
                    text_to_add = ""
                    listening_for_keys = False

            elif event.key == pygame.K_ESCAPE and not listening_for_size_change and listening_for_keys:
                listening_for_size_change = True

            elif listening_for_size_change and event.key == pygame.K_ESCAPE:
                listening_for_size_change = False

                size_to_change = ""

            elif event.key == pygame.K_BACKSPACE:
                if listening_for_size_change:
                    size_to_change = size_to_change[:-1]

                    try:
                        if cond_check():
                            main.current_text.size = int(size_to_change)
                        else:
                            x.size = int(size_to_change)
                    except Exception:
                        print('An error occurred while trying to change the size.')
                        size_to_change = ""   

                elif listening_for_keys:
                    text_to_add = text_to_add[:-1]
                    
                    
            elif listening_for_size_change:
                size_to_change += event.unicode

                try:
                    if cond_check():
                        main.current_text.size = int(size_to_change)
                    else:
                        x.size = int(size_to_change)
                except Exception:
                    print('An error occurred while trying to change the size.')
                    size_to_change = ""

            elif listening_for_keys and not listening_for_size_change:
                text_to_add += event.unicode
                if cond_check():
                    main.current_text.text = text_to_add
                else:
                    x.text = text_to_add
                
            # rects

            elif event.unicode == 'e':
                x = RECT(25, 25, 100, 50, main)
                x.index = len(main.rects)-1
                main.rects.append(x)                
            
            elif event.unicode == 'r':
                try:
                    del main.rects[main.current_rect.index]
                except Exception:
                    pass
            
            elif event.unicode == 's':
                data.save_data()

            elif event.unicode == 'c':
                data.clear_data()


    main.display()
