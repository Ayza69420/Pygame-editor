import os

try:
    import pygame
except ModuleNotFoundError:
    os.system("pip3 install pygame")    
    print("Pygame auto installation finished, you may restart the program now.")
except ImportError:
    os.system("pip3 install pygame")    
    print("Pygame auto installation finished, you may restart the program now.")

print("Instructions can be found at: https://github.com/Ayza69420/Pygame-editor/blob/main/README.md")

import main.main_loop
