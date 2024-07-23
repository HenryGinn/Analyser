import os

from preprocess import Preprocess


class Chat(Preprocess):

    def __init__(self, whatsapp, name):
        self.whatsapp = whatsapp
        self.name = name
        self.set_paths()

    def set_paths(self):
        self.path_folder = self.whatsapp.get_path(self.name)
        self.path_chat = os.path.join(self.path_folder,
                                      "_chat.txt")

    def preprocess(self):
        self.construct_dataframe()
