# Pygame editor

Pygame editor is made to help you visualize UI in pygame, which will make creating UI much easier. still work in progress.

# Instructions

All you gotta do is run the `main.py` file. When done using the program, all the objects details will be provided in the ``info.txt`` file automatically which can be found in the ``main`` folder, however, if you wanna save the states of each object, you can use the **M** hotkey to open the menu as listed below in the hotkeys and use the save data button.

The purpose of ``updater.py`` is checking whether there are any new updates relying on the ``version.txt``, if there are, it'll prompt you whether you wanna update or not.

# Installation

- Clone with git using the following command: ```git clone https://github.com/Ayza69420/Pygame-editor.git```
- Run ``cd Pygame-editor``
- Run ``pip install -r requirements.txt`` to install any required libraries

# Hotkeys

***MAIN HOTKEYS***

- *M = Menu*  
  - Save data
  - Clear data
  - Erase
  - Settings
  - Object color changing
  - Font changer
- *Z = Redo*  
- *Y = Undo*  
- *C = Copy*
- *V = Paste*  
- *X = Cut*  

***OBJECTS HOTKEYS***  

- *E = Create New Rect*  
- *T = Create text*  
  - If you're hovering over an existing text object, it'll instead edit it
- *R = Remove Object*  
- *F = Fill*
  - Fills whatever you're hovering over with the color you're using
  - Colorable objects: Text, Rect, Background

***TEXT EDITING HOTKEYS***

- *Backspace = Removes*  
- *Enter = Finish/End*  
- *Escape (esc) = Change text size*  
  - Adds 1 to the size if you press **+**
  - Removes 1 from the size if you press **-**
  - Size cannot be greater than 100
- *Escape (esc) again = Finish changing text size*  


# Main To-do

- ~~Add rect coloring in the menu~~
  - ~~Add filling~~
- ~~Create Menu~~
- ~~Create settings~~  
- ~~Create Updater~~
- ~~Add text font changing~~
- ~~Create Copy, paste and cut~~
- ~~Ability to get everything's information on close~~
- ~~Saving~~
