from os import system
from sys import platform
from json import loads

def main():
    with open("./main/settings.json") as sett:
        auto_update = loads(sett.read())["auto_update"]

    try:
        import pygame
    except ModuleNotFoundError:
        system("pip3 install pygame")    
        print("Pygame auto installation finished, you may restart the program now.")
    except ImportError:
        system("pip3 install pygame")    
        print("Pygame auto installation finished, you may restart the program now.")

    print("Instructions can be found at: https://github.com/Ayza69420/Pygame-editor/blob/main/README.md")

    if auto_update:
        if platform.lower() in ("linux", "linux2"):
            system("python3 updater.py")
        else:
            system("python updater.py")

    import main.main_loop

if __name__ == "__main__":
    main()
