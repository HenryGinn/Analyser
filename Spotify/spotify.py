from os.path import join

import pandas as pd
from hgutilities.utils import make_folder

from Processing.preprocess_spotify import PreprocessSpotify
from Output.output_series import OutputSeries


class Spotify(PreprocessSpotify, OutputSeries):

    def __init__(self, path, months_back=None):
        self.set_paths(path)
        self.months_back = months_back

    def set_paths(self, path):
        self.path_base = path
        self.path_dataframe = join(self.path_base, "Data.pkl")
        self.path_csv = join(self.path_base, "Data.csv")
        self.path_output = join(self.path_base, "Output")
        make_folder(self.path_output)

    def top_key(self, attribute):
        df_key = self.df.loc[:, [attribute, "Count"]].copy()
        df_key = df_key.set_index(attribute)
        df_key = df_key.groupby(df_key.index).sum()
        df_key = df_key.sort_values("Count", ascending=False)
        self.output_series(df_key, f"Most Played {attribute}s")
        return df_key
