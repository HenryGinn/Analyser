from os.path import join

from Processing.preprocess_spotify import PreprocessSpotify


class Spotify(PreprocessSpotify):

    def __init__(self, path):
        self.set_paths(path)

    def set_paths(self, path):
        self.path_base = path
        self.path_dataframe = join(self.path_base, "Data.pkl")
        self.path_csv = join(self.path_base, "Data.csv")
