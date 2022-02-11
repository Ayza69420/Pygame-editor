import json
import requests
import os

path = os.path.split(os.path.realpath(__file__))[0] # Path to the current directory

directory_files = [os.listdir(path), os.listdir(path+"\\main")] # Used to compare between the directory & repo files to find new files

version = requests.get("https://raw.githubusercontent.com/Ayza69420/Pygame-editor/main/version.txt").text.strip() # Repo version

repo_files = requests.get("https://api.github.com/repos/Ayza69420/Pygame-editor/git/trees/main?recursive=1").json()

def update():
    for repo_file in repo_files["tree"]:
        if repo_file["mode"] == 100644:
            file_path = repo_file["path"]
            content = requests.get(f"https://raw.githubusercontent.com/Ayza69420/Pygame-editor/main/{file_path}").text
            
            if file_path == "main/settings.json": # This is to not mess up the user's current set settings, just adds the new settings.
                with open(path+file_path, "r+") as f:
                    settings = json.loads(requests.get(f"https://raw.githubusercontent.com/Ayza69420/Pygame-editor/main/main/settings.json").text)
                    user_settings = json.loads(f.read())

                    if len(user_settings) != len(settings):
                        print("Updating main/settings.json..")
                        for i in settings:
                            if i not in user_settings:
                                user_settings[i] = settings[i]

                        f.write(user_settings)

            elif repo_file in directory_files:
                with open(path+file_path, "r+") as f:
                    if content != f.read():
                        print(f"Updating {file_path}..")
                    
                        f.write(content)

            elif repo_file not in directory_files[0] and repo_file not in directory_files[1]:
                print(f"Adding {file_path}..")

                with open(path+file_path, "x") as f:
                    with open(path+file_path, "w") as f:
                        f.write(content)

    with open(path+"version.txt", "w") as ver:
        ver.write(version)

with open(path+"\\version.txt", "r") as ver:
    if ver.read() == version:
        input("No available updates.")
    else:
        if input("An update was found. Proceed on updating? Y/N\n").lower() == "y":
            update()
        else:
            exit()
