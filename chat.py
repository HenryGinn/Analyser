from os.path import join

from preprocess import Preprocess
from people import People


class Chat(Preprocess, People):

    def __init__(self, whatsapp, name):
        self.whatsapp = whatsapp
        self.name = name
        self.set_paths()

    def set_paths(self):
        self.path_folder = self.whatsapp.get_path(self.name)
        self.path_chat_original = join(
            self.path_folder, "_chat.txt")
        self.path_chat = join(self.path_folder, "Chat.pkl")
