import os


class Chat():

    def __init__(self, whatsapp, name):
        self.whatsapp = whatsapp
        self.name = name
        self.set_path()

    def set_path(self):
        self.path = os.path.join(self.whatsapp.path_base,
                                 self.name)

    def preprocess(self):
        print(f"Preprocessing {self.name}")
