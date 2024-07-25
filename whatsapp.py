import os

from hgutilities import defaults

from chat import Chat


class WhatsApp():

    def __init__(self, path):
        self.path_base = path
        self.chat_objects = {}

    def get_path(self, name):
        path = os.path.join(self.path_base, name)
        return path

    def initialise_chats(self):
        for name in os.listdir(self.path_base):
            self.initialise_chat(name)

    def initialise_chat(self, name):
        chat_obj = Chat(self, name)
        self.chat_objects.update({name: chat_obj})

    def process(self, function, **kwargs):
        for chat_name in self.chat_objects:
            self.process_chat(chat_name, function, **kwargs)

    def process_chat(self, chat_name, function, **kwargs):
        chat_obj = self.chat_objects[chat_name]
        defaults.kwargs(chat_obj, kwargs)
        chat_method = getattr(chat_obj, function)
        chat_method()
        chat_obj.force = False
