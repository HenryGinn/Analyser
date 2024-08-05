from os.path import join

import pandas as pd

from hgutilities import defaults
from hgutilities.utils import make_folder

from Processing.preprocess_spotify import PreprocessSpotify
from Output.output_series import OutputSeries


class Spotify(PreprocessSpotify, OutputSeries):

    def __init__(self, path, **kwargs):
        defaults.kwargs(self, kwargs)
        self.set_paths(path)

    def set_paths(self, path):
        self.path_base = path
        self.path_dataframe = join(self.path_base, "Data.pkl")
        self.path_csv = join(self.path_base, "Data.csv")

    def filter_time(self):
        self.set_start_date()
        self.set_end_date()
        self.df = self.df[self.start_date:self.end_date]
        self.set_title_date()
        self.set_output_path()

    def set_start_date(self):
        if self.start_date is None:
            self.start_date = self.df.index[0]
        elif isinstance(self.start_date, int):
            offset = pd.DateOffset(months=self.start_date)
            self.start_date = self.df.index[-1] - offset

    def set_end_date(self):
        if self.end_date is None:
            self.end_date = self.df.index[-1]
        elif isinstance(self.end_date, int):
            offset = pd.DateOffset(months=self.end_date)
            self.end_date = self.df.index[-1] - offset
    
    def set_output_path(self):
        start = self.start_date.strftime("%B %Y")
        end = self.end_date.strftime("%B %Y")
        time_folder_name = f"{start} - {end}"
        self.path_output = join(self.path_base, "Output", time_folder_name)
        make_folder(self.path_output)

    def top_count(self, attribute):
        df_count = self.df.loc[:, [attribute, "Count"]].copy()
        df_count = df_count.set_index(attribute)
        df_count = df_count.groupby(df_count.index).sum()
        df_count = df_count.sort_values("Count", ascending=False)
        self.output_series(df_count, f"Most Played {attribute}s by Frequency",
                           y_label="Frequency")
        return df_count

    def top_time(self, attribute):
        df_time = self.df.loc[:, [attribute, "TimePlayed"]].copy()
        df_time = df_time.set_index(attribute)
        df_time = df_time.groupby(df_time.index).sum()
        df_time = df_time.sort_values("TimePlayed", ascending=False)
        df_time.loc[:, "TimePlayed"] = (df_time["TimePlayed"] / 3600000).round()
        self.output_series(df_time, f"Most Played {attribute}s by Time Played",
                           y_label="Time Played (hours)")
        return df_time

    def histogram(self, attribute):
        df_hist = self.df.loc[:, [attribute, "TimePlayed"]].copy()
        top_entries = self.get_top_entries(attribute, df_hist)
        for entry in top_entries:
            self.histogram_entry(df_hist, attribute, entry)

    def get_top_entries(self, attribute, df):
        top_entries = (df.groupby(attribute).sum()
                       .sort_values("TimePlayed", ascending=False)
                       .iloc[:1, 0].index.values)
        return top_entries

    def histogram_entry(self, df_hist, attribute, entry):
        df_hist = df_hist.loc[df_hist[attribute] == entry].copy()
        self.initiate_figure()
        self.ax.hist(df_hist["TimePlayed"].values, bins=100)
        self.output_figure("Test")


defaults.load(Spotify)
