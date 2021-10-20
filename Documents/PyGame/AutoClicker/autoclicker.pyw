import os

os.system('pip install pygame')
os.system('pip install pyautogui')

import pygame
import pygame.draw
import pygame.font
import sys
from threading import Thread
from pynput import keyboard
from pynput.mouse import Button, Controller
import time

pygame.init()

WIDTH = 500
HEIGHT = 350
FPS = 60

mouse = Controller()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Autoclicker')
clock = pygame.time.Clock()

Path = os.path.dirname(os.path.realpath(__file__))

try:
    assert('Akzidenz-grotesk-roman.ttf' in os.listdir(Path))
except AssertionError:
    sys.exit('Make sure the font is in the same directory.')

texts = {
    'input_text1': '',
    'input_text2': '',
    'input_text3': '',
    'input_text4': '',
    'input_text5': ''
}

active = 0

class MAIN:
    def __init__(self):
        self.bg_color = pygame.Color('grey11')
        self.outlines_color = pygame.Color('grey20')
        self.box_color = pygame.Color('grey25')
        self.right_on = False
        self.left_on = False
        self.fast_on = False
        self.started = False
        self.awaited_time = 0
        self.safemode = open(f'{Path}/safemode.txt','r').readlines()

    def display(self):
        global active

        window.fill(self.bg_color)
        self.outlines()
        self.boxes()
        self.buttons()

        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',16).render(texts['input_text1'],False,(255,255,255)),(self.milliseconds.x + 4,self.milliseconds.y + 5))
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',16).render(texts['input_text2'],False,(255,255,255)),(self.seconds.x + 4,self.seconds.y + 5))
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',16).render(texts['input_text3'],False,(255,255,255)),(self.minutes.x + 4,self.minutes.y + 5))
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',16).render(texts['input_text4'],False,(255,255,255)),(self.hours.x + 4,self.hours.y + 5))
        
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',14).render('Rmouse',False,(255,255,255)),(self.rmouse.x - 12,self.rmouse.y - 30))
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',14).render('Lmouse',False,(255,255,255)),(self.lmouse.x - 12,self.lmouse.y - 30))
        
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',18).render('Fast Mode',False,(255,255,255)),(370,300))
        
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',21).render((f'time: {main.awaited_time}'),False,(255,255,255)),(0,HEIGHT-21))

    def outlines(self):
        xcoor_space = 10
        top_width = WIDTH-(xcoor_space*2)
        height = 5

        self.height = height    
        self.xcoor_space = xcoor_space

        upper_line = pygame.draw.rect(window,self.outlines_color,pygame.Rect(xcoor_space,10,top_width,height),3)
        upper_one = pygame.draw.rect(window,self.outlines_color,pygame.Rect(xcoor_space,15,5,height*2),3)
        upper_two = pygame.draw.rect(window,self.outlines_color,pygame.Rect(WIDTH-(xcoor_space*1.5),15,5,height*2),3)
        
        lower_line = pygame.draw.rect(window,self.outlines_color,pygame.Rect(xcoor_space,70,top_width,height),3)
        lower_one = pygame.draw.rect(window,self.outlines_color,pygame.Rect(xcoor_space,60,5,height*2),3)
        lower_two = pygame.draw.rect(window,self.outlines_color,pygame.Rect(WIDTH-(xcoor_space*1.5),60,5,height*2),3)

        self.one = upper_one
        self.two = upper_two
        #===============================================================================================================#
        upper_line2 = pygame.draw.rect(window,self.outlines_color,pygame.Rect(xcoor_space,150,125,height),3)
        upper_three = pygame.draw.rect(window,self.outlines_color,pygame.Rect(xcoor_space,155,5,height*2),3)
        upper_four = pygame.draw.rect(window,self.outlines_color,pygame.Rect(upper_line2.right-6,155,5,height*2),3)

        lower_line2 = pygame.draw.rect(window,self.outlines_color,pygame.Rect(xcoor_space,270,125,height),3)
        lower_three = pygame.draw.rect(window,self.outlines_color,pygame.Rect(xcoor_space,260,5,height*2),3)
        lower_four = pygame.draw.rect(window,self.outlines_color,pygame.Rect(lower_line2.right-6,260,5,height*2),3)

        self.three = lower_three
        self.four = lower_four


    def boxes(self):
        # +125 x/box
        self.hours = pygame.draw.rect(window,self.box_color,pygame.Rect(self.one.x + 15, self.one.y + 10, 75, self.one.height*2),3)
        self.minutes = pygame.draw.rect(window,self.box_color,pygame.Rect(self.one.x + 140, self.one.y + 10, 75, self.one.height*2),3)
        self.seconds = pygame.draw.rect(window,self.box_color,pygame.Rect(self.one.x + 265, self.one.y + 10, 75, self.one.height*2),3)
        self.milliseconds = pygame.draw.rect(window,self.box_color,pygame.Rect(self.one.x + 390, self.one.y + 10, 75, self.one.height*2),3)

        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',16).render('Milliseconds',False,(96, 137, 180)),(self.milliseconds.x,self.milliseconds.y+30))
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',16).render('Seconds',False,(96, 137, 180)),(self.seconds.x+10,self.seconds.y+30))
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',16).render('Minutes',False,(96, 137, 180)),(self.minutes.x+14,self.minutes.y+30))
        window.blit(pygame.font.Font(f'{Path}/Akzidenz-grotesk-roman.ttf',16).render('Hours',False,(96, 137, 180)),(self.hours.x+17,self.hours.y+30))
        

    def update_time(self):
        main.awaited_time = 0

        if texts['input_text1']: main.awaited_time += int(texts['input_text1'])/1000
        if texts['input_text2']: main.awaited_time += int(texts['input_text2'])
        if texts['input_text3']: main.awaited_time += (60)*int(texts['input_text3'])
        if texts['input_text4']: main.awaited_time += (60*60)*int(texts['input_text4'])

    
    def buttons(self):
        if self.left_on:
            self.on_left = (29, 185, 84)
        else:
            self.on_left = self.outlines_color

        if self.right_on:
            self.on_right = (29, 185, 84)
        else:
            self.on_right = self.outlines_color

        if self.fast_on:
            self.on_fast = (29, 185, 84)
        else:
            self.on_fast = self.outlines_color

        left_mouse_button = pygame.draw.rect(window,self.on_left,pygame.Rect(self.xcoor_space+20,200,25,self.height*12),4)
        right_mouse_button = pygame.draw.rect(window,self.on_right,pygame.Rect(self.xcoor_space+80,200,25,self.height*12),4)
        extra_fast_button = pygame.draw.rect(window,self.on_fast,pygame.Rect(363,325,100,50),3)

        self.fast = extra_fast_button
        self.lmouse = left_mouse_button
        self.rmouse = right_mouse_button

    def start_loop(self,fast_mode=False):
        count = 0
        if int(main.awaited_time) == 0 and self.safemode[0].lower() == 'true':
            main.awaited_time = 0.001
        if fast_mode:
            while self.started:
                count += 1
                if self.right_on:
                    mouse.click(Button.right, 2)
                elif self.left_on:
                    mouse.click(Button.left, 2)

                time.sleep(main.awaited_time)
        else:
            while self.started:
                count += 1
                if self.right_on:
                    mouse.press(Button.right)
                elif self.left_on:
                    mouse.press(Button.left)

                time.sleep(main.awaited_time)        

    def start(self):
        if self.fast_on:
            Thread(target=self.start_loop,args=(True,)).start()
        else:
            Thread(target=self.start_loop).start()


main = MAIN()

def on_press(key):
    if key == keyboard.Key.delete and not main.started:
        main.started = True
        main.start()
    else:
        main.started = False
        
listener = keyboard.Listener(on_press=on_press)
listener.start()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if main.lmouse.collidepoint(pos):
                if main.left_on:
                    main.left_on = False
                elif not main.left_on and not main.right_on:
                    main.left_on = True

            elif main.rmouse.collidepoint(pos):
                if main.right_on:
                    main.right_on = False
                elif not main.right_on and not main.left_on:
                    main.right_on = True

            elif main.fast.collidepoint(pos):
                if main.fast_on:
                    main.fast_on = False
                else:
                    main.fast_on = True

            elif main.milliseconds.collidepoint(pos):
                active = 1
            elif main.seconds.collidepoint(pos):
                active = 2
            elif main.minutes.collidepoint(pos):
                active = 3
            elif main.hours.collidepoint(pos):
                active = 4
            else:
                active = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and active != 0:
                texts[f'input_text{active}'] = texts[f'input_text{active}'][:-1]
                main.update_time()

            elif event.key == pygame.K_RETURN:
                active = 0
            else:
                if event.unicode.isdigit() and len(texts[f'input_text{active}'])<=7 and active != 0:
                    texts[f'input_text{active}'] += event.unicode
                    main.update_time()


    main.display()
    pygame.display.update()
