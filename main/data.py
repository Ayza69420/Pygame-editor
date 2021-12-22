import json
import os

from main.objects import RECT, TEXT

class data:
    def __init__(self, main):
        self.main = main

    def get_data(self):
        try:
            with open(f"{os.path.split(os.path.realpath(__file__))[0]}\\data.json", "r") as data:
                data = json.loads(data.read())

                if data:
                    for i in data:
                        if i["type"] == "rect":
                            x = RECT(i["x"],i["y"],i["width"],i["height"],self.main,i["color"])
                            self.main.rects.append(x)

                        elif i["type"] == "text":
                            x = TEXT(i["size"],i["text"],self.main,i["x"],i["y"])
                            self.main.text.append(x)
        except Exception as err:
            with open(f"{os.path.split(os.path.realpath(__file__))[0]}\\data.json","w") as data:
                data.write(json.dumps([]))

                print("Failed to retrieve data.")
                self.main.debug(err)

    def save_data(self):
        with open("data.json", "w") as data:
            try:
                data_to_write = []

                if self.main.rects:
                    for i in self.main.rects:
                        data_to_write.append({"x": i.x, "y": i.y, "width": i.width, "height": i.height, "color": i.color, "type": "rect"})

                if self.main.text:
                    for i in self.main.text:
                        data_to_write.append({"size": i.size, "text": i.text, "x": i.x, "y": i.y, "type": "text"})

                data.write(json.dumps(data_to_write))

                print("Successfully saved.")

            except Exception as err:
                with open(f"{os.path.split(os.path.realpath(__file__))[0]}\\data.json","w") as data:
                    data.write(json.dumps([]))

                    print("Failed to save the data")
                    self.main.debug(err)

    def clear_data(self):
        with open(f"{os.path.split(os.path.realpath(__file__))[0]}\\data.json", "w") as data:
            data.write(json.dumps([]))

            print("Successfully cleared the data")
