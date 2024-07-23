import re

import pandas as pd


class Preprocess():

    def construct_dataframe(self):
        self.extract_data_from_file()
        self.initialise_chat_dict()
        self.populate_chat_dict()
        self.create_dataframe()
        self.filter_initial_messages()

    def extract_data_from_file(self):
        pattern = r'[\u200e\u200f\u202a\u202b\u202c\u202d\u202e\n\r]'
        with open(self.path_chat, "r") as file:
            self.data = [re.sub(pattern, '', line)
                         for line in file]

    def initialise_chat_dict(self):
        self.chat_dict = {"Timestamp": [],
                          "Sender": [],
                          "Content": [],
                          "Photo": []}

    def populate_chat_dict(self):
        message = [self.data[0]]
        for line in self.data:
            if self.message_start(line):
                self.process_message(message)
                message = [line]
            else:
                message.append(line)

    def message_start(self, line):
        pattern = r"\[\d{2}/\d{2}/\d{4}, \d{2}:\d{2}:\d{2}\]"
        starts_with_timestamp = bool(re.search(pattern, line[:22]))
        return starts_with_timestamp

    def contains_photo(self, line):
        pattern = (r"<attached: \d{8}-(GIF|PHOTO)-\d{4}-\d{2}"
                   r"-\d{2}-\d{2}-\d{2}-\d{2}\.(mp4|jpg)>")
        photo = bool(re.search(pattern, line)) or (line == "image omitted")
        return photo

    def process_message(self, message):
        timestamp, name, message = self.process_first_line(message)
        photo = self.contains_photo(message[0])
        message = "\t".join(message)
        self.update_chat_dict(timestamp, name, message, photo)

    def process_first_line(self, message):
        timestamp = message[0][:22]
        colon_index = message[0][22:].index(":") + 22
        name = message[0][23:colon_index]
        message[0] = message[0][colon_index+2:]
        return timestamp, name, message

    def update_chat_dict(self, timestamp, name, message, photo):
        self.chat_dict["Timestamp"].append(timestamp)
        self.chat_dict["Sender"].append(name)
        self.chat_dict["Photo"].append(photo)
        self.chat_dict["Content"].append(message)

    def create_dataframe(self):
        data_types = {"Sender": "category", "Photo": "bool", "Content": "object"}
        self.df = pd.DataFrame(self.chat_dict).astype(data_types)
        self.df["Timestamp"] = pd.to_datetime(
            self.df["Timestamp"], format="[%d/%m/%Y, %H:%M:%S]")
        self.df = self.df.set_index("Timestamp").reindex(columns=data_types.keys())

    def filter_initial_messages(self):
        message = ("Messages and calls are end-to-end encrypted. "
                   "No one outside of this chat, not even "
                   "WhatsApp, can read or listen to them.")
        self.df = self.df.loc[self.df["Content"] != message]
