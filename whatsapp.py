import os

from chat import Chat


class WhatsApp():

    def __init__(self, path):
        self.path_base = path
        self.chat_objects = {}
        self.set_chat_names()

    def update_folder_names(self):
        for old_name in os.listdir(self.path_base):
            if "WhatsApp Chat - " in old_name:
                self.update_folder_name(old_name)
        self.set_chat_names()

    def update_folder_name(self, old_name):
        new_name = old_name[16:]
        old_path = self.get_path(old_name)
        new_path = self.get_path(new_name)
        os.rename(old_path, new_path)

    def get_path(self, name):
        path = os.path.join(self.path_base, name)
        return path

    def set_chat_names(self):
        self.chat_names = [name for name
                           in os.listdir(self.path_base)]

    def initialise_chats(self):
        for name in self.chat_names:
            self.initialise_chat(name)

    def initialise_chat(self, name):
        chat_obj = Chat(self, name)
        self.chat_objects.update({name: chat_obj})

    def process(self, function):
        for chat_name in self.chat_objects:
            self.process_chat(chat_name, function)

    def process_chat(self, chat_name, function):
        chat_obj = self.chat_objects[chat_name]
        chat_method = getattr(chat_obj, function)
        chat_method()
