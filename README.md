# Pygame editor

Pygame editor is made to help you visualize UI in pygame, which will make creating UI much easier.

# Instructions

All you gotta do is run the `main.py` file. When done using the program, all the objects details will be provided in the ``info.txt`` file automatically which can be found in the ``main`` folder, however, if you wanna save the states of each object, you can use the **M** hotkey to open the menu as listed below in the hotkeys and use the save data button.

The purpose of ``updater.py`` is providing optional update checking, if there are available updates, it'll prompt you whether you wanna update or not. You can enable automatic updating through settings **(Menu -> Settings)** which will always check for updates when you run the program, whuch unlike running the ``updater.py``, this won't contain any inputs.

# Installation

- Clone the repository with git using ```git clone https://github.com/Ayza69420/Pygame-editor.git```
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
  - Increments the size by one if you press **+**
  - Decrements the size by one if you press **-**
  - Size cannot be greater than 100
- *Escape (esc) again = Finish changing text size*  

# Menu

- Save data
  - Saves everything in the `data.json` file in a format the program can understand
- Clear data
  - Clears the data safely to avoid errors
- Erase
  - Erases everything, cannot be undone
- RGB Color
  - Contains 3 text boxes (R, G, B) in a sorted order
  - Clicking on any button and typing in numbers **(Cannot be greater than 255)** will change any new object's color, you will have to press enter to confirm
- Font
  - Changes text font to the font you specify
  - The text you input is **Case sensitive** and **Must contain the full name with the file extension**
  - If an invalid font was given, it'll automatically use the default font specificed in the `settings.json` file **(Can be found in the `main` folder)**
  - The font file **must be in the `Fonts` folder** which can be found inside of the `main` folder.
- Settings
  - Auto save: Will automatically save if you close the program
  - Debug Mode: Saves any errors with the timestamp in the `debug.txt` file which can be found in the `main` folder
  - Auto update: Will automatically update as soon as you run the program
