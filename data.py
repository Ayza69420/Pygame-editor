import json

class data:
    def __init__(self, rect, main):
        self.rect = rect
        self.main = main

    def get_data(self):
        with open('data.json', 'r') as data:
            data = json.loads(data.read())

            if data != None:
                for i in data:
                    x = self.rect(i['x'],i['y'],i['width'],i['height'],self.main)
                    self.main.rects.append(x)
                    self.main.rects[len(self.main.rects)-1].index = len(self.main.rects)-1

    def save_data(self):
        with open('data.json', 'w') as data:
            data_to_write = []

            for i in self.main.rects:
                data_to_write.append({'x': i.x, 'y': i.y, 'width': i.width, 'height': i.height})

            data.write(json.dumps(data_to_write))

    def clear_data(self):
        with open('data.json', 'w') as data:
            data.write(json.dumps([]))