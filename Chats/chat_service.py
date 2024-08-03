import os

from hgutilities import defaults

from Elements.chat import Chat


class ChatService():

    def __init__(self, path):
        self.path_base = path
        self.chat_objects = []

    def initialise_chats(self):
        for name in os.listdir(self.path_base):
            self.initialise_chat(name)

    def process(self, function, **kwargs):
        for chat_obj in self.chat_objects:
            self.process_chat(chat_obj, function, **kwargs)

    def process_chat(self, chat_obj, function, **kwargs):
        defaults.kwargs(chat_obj, kwargs)
        chat_method = getattr(chat_obj, function)
        chat_method()
        chat_obj.force = False
