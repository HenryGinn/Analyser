from hgutilities import defaults

from Output.output import Output


class TimeSeries(Output):

    def plot_time_series_date(self, df, name, x_label, y_label):
        self.initialise_figure()
        df = self.get_time_series_date(df)
        self.ax.plot(df, color=self.color_1)
        self.set_peripherals(self.ax, name, x_label, y_label)
        self.output_figure(name)

    def get_time_series_date(self, df):
        df = df.loc[:, "Count"].copy()
        df = df.resample("D").sum()
        df = df.rolling(14, center=True).mean().dropna()
        return df


defaults.load(TimeSeries)
