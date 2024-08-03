import pandas as pd
from re import split
from numpy import sqrt

from Elements.base import Base


class People(Base):

    def people(self):
        self.initialise_people_dataframe()
        self.set_messages_dataframe()
        self.add_person_messages_sent()
        self.add_person_word_counts_and_means()
        self.add_person_word_standard_deviations()


    # Constructing dataframes of messages and data by person

    def initialise_people_dataframe(self):
        self.people_list = list(set(self.df["Sender"].values))
        self.df_people = pd.DataFrame(index=self.people_list)

    def set_messages_dataframe(self):
        self.df_messages = self.df.copy()
        self.df_messages["Count"] = 1
        self.add_messages_dataframe_squared_sum_words()
        self.add_messages_dataframe_squared_sum_characters()
        self.aggregate_messages_dataframe()

    def add_messages_dataframe_squared_sum_words(self):
        self.df_messages["Squared Sum Words"] = (
            self.df_messages["Content"].apply(
                lambda x: len(x.split())**2))

    def add_messages_dataframe_squared_sum_characters(self):
        self.df_messages["Squared Sum Characters"] = (
            self.df_messages["Content"].apply(
                lambda x: sum(len(word)**2 for word in x.split())))

    def aggregate_messages_dataframe(self):
        agg_functions = {key: "sum" for key in self.df_messages.columns.values}
        agg_functions["Content"] = lambda x: " ".join(x)
        del agg_functions["Sender"]
        self.df_messages = self.df_messages.groupby(
            "Sender", observed=True).aggregate(agg_functions)

    
    # Counts and Averages
    
    def add_person_messages_sent(self):
        self.df_people["Messages Sent"] = self.df_messages["Count"].copy()
        self.df_people["Photos Sent"] = self.df_messages["Photo"].copy()

    def add_person_word_counts_and_means(self):
        self.add_person_word_count()
        self.add_person_words_per_message()
        self.add_person_character_count()
        self.add_person_characters_per_word()
        self.add_person_characters_per_message()

    def add_person_word_count(self):
        self.df_people["Word Count"] = (
            self.df_messages["Content"]
            .apply(lambda x: len(x.split())))

    def add_person_words_per_message(self):
        self.df_people["Words per Message"] = (
            self.df_people["Word Count"] /
            (self.df_people["Messages Sent"] -
             self.df_people["Photos Sent"]))

    def add_person_character_count(self):
        self.df_people["Character Count"] = (
            self.df_messages["Content"]
            .apply(lambda x: len(x)))

    def add_person_characters_per_word(self):
        self.df_people["Characters per Word"] = (
            (self.df_people["Character Count"] -
             self.df_people["Word Count"]) /
            self.df_people["Word Count"])

    def add_person_characters_per_message(self):
        self.df_people["Characters per Message"] = (
            self.df_people["Character Count"] /
            self.df_people["Messages Sent"])


    # Standard deviations

    def add_person_word_standard_deviations(self):
        self.add_person_std_chars_per_word()
        #self.add_person_std_chars_per_message()
        self.add_person_std_words_per_message()

    def add_person_std_chars_per_word(self):
        self.df_people["Standard Deviation of Characters per Word"] = sqrt(
            self.df_messages["Squared Sum Characters"] /
            self.df_people["Word Count"] -
            self.df_people["Characters per Word"]**2)

    def add_person_std_chars_per_message(self):
        self.df_people["Standard Deviation of Characters per Message"] = sqrt(
            self.df_messages["Squared Sum Characters"] /
            self.df_people["Messages Sent"] -
            self.df_people["Characters per Message"]**2)

    def add_person_std_words_per_message(self):
        self.df_people["Standard Deviation of Words Per Message"] = sqrt(
            self.df_messages["Squared Sum Words"] /
            self.df_people["Messages Sent"] -
            self.df_people["Words per Message"]**2)
