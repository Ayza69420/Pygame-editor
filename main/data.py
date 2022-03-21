import json
import os

from main.objects import RECT, TEXT

data_file = "%s/data.json" % os.path.split(os.path.realpath(__file__))[0]

class data:
    def __init__(self, main):
        self.main = main

    def get_data(self):
        try:
            with open(data_file, "r") as data:
                data = json.loads(data.read())

                if data:
                    for i in data:
                        if "background_color" in i:
                            self.main.window_color = i["background_color"]
                            
                        elif i["type"] == "rect":
                            try:
                                x = RECT(i["x"],i["y"],i["width"],i["height"],self.main,i["color"])
                                self.main.rects.append(x)
                            except Exception as err:
                                self.main.debug(err, "(Line 27,, data.py)")

                        elif i["type"] == "text":
                            try:
                                x = TEXT(i["size"],i["text"],self.main,i["x"],i["y"], i["font"])
                                self.main.text.append(x)
                            except Exception as err:
                                self.main.debug(err)
                                
        except Exception as err:
            with open(data_file,"w") as data:
                data.write(json.dumps([]))

                print("Failed to retrieve data.")
                self.main.debug(err)

    def save_data(self):
        with open(data_file, "w") as data:
            try:
                data_to_write = []

                data_to_write.append({"background_color": self.main.window_color})

                if self.main.rects:
                    for i in self.main.rects:
                        data_to_write.append({"x": i.x, "y": i.y, "width": i.width, "height": i.height, "color": i.color, "type": "rect"})

                if self.main.text:
                    for i in self.main.text:
                        data_to_write.append({"size": i.size, "text": i.text, "x": i.x, "y": i.y, "font": i.font, "type": "text"})

                data.write(json.dumps(data_to_write))

                print("Successfully saved.")

            except Exception as err:
                with open(data_file,"w") as data:
                    data.write(json.dumps([]))

                    print("Failed to save the data")
                    self.main.debug(err)

    def clear_data(self):
        with open(data_file, "w") as data:
            data.write(json.dumps([]))

            print("Successfully cleared the data")
