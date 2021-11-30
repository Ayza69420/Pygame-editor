import pygame
from threading import Thread
from data import data
from objects import RECT

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

        self.current_rect = RECT(25, 25, 100, 50, self)
        self.rects = [self.current_rect] 


    def display(self):
        self.window.fill((255,255,255))
        self.create_rect()
        self.render_text()


        pygame.display.update()
        self.clock.tick(60)

    def render_text(self):
        font = pygame.font.SysFont('freesansbold.ttf',32)
        text = font.render(f'Position: ({self.current_rect.x},{self.current_rect.y}) | Size:  (Width: {self.current_rect.width} | Height: {self.current_rect.height})',False,(0,0,0))

        self.window.blit(text, (10, self.window_height-25))

    def create_rect(self):
        for rect in self.rects:
            rect.create()


main = MAIN()
data = data(main)

data.get_data()

selected = False
dragging = False

print("""
|  HOTKEYS  
| S = Save Data
| C = Clear Data	    
| E = Create New Rect
| R = Remove Rect
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

                    def change_pos():
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


                    Thread(target=change_pos).start()

        if event.type == pygame.MOUSEBUTTONUP and dragging == True:
            dragging = False

        if event.type == pygame.KEYDOWN:
            if event.unicode == 'e':
                x = RECT(25, 25, 100, 50, main)
                main.rects.append(x)
                main.rects[len(main.rects)-1].index = len(main.rects)-1
                
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
