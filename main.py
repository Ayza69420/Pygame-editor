import os

try:
    import pygame
except ModuleNotFoundError:
    os.system("pip3 install pygame")    
    print("Pygame auto installation finished, you may restart the program now.")
except ImportError:
    os.system("pip3 install pygame")    

    print("Pygame auto installation finished, you may restart the program now.")

print("""
| HOTKEYS  
|
| M = Menu  
| Z = Redo
| Y = Undo
| C = Copy
| V = Paste
| X = Cut
|
| OBJECTS HOTKEYS
|
| T = Create text T = Create text (This won't create text if you select on an existing text and hover over it, instead edit it)
| E = Create New Rect
| R = Remove Object
| F = Fill
|
| TEXT CONTROL HOTKEYS
|
| Backspace = Removes text
| Enter = Finish/End
| Escape (esc) = Change text size 
| Escape (esc) again = Finish/End Changing
""")

import main.main_loop
