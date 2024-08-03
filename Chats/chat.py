from os.path import join

from Processing.preprocess_whatsapp import PreprocessWhatsapp
from Processing.people import People


class Chat(People):

    def __init__(self, service, name):
        self.service = service
        self.name = name

    def set_paths(self):
        self.path_folder = self.service.get_path_chat(self.name)
        self.path_chat_original = join(
            self.path_folder, "_chat.txt")
        self.path_chat = join(self.path_folder, "Chat.pkl")
