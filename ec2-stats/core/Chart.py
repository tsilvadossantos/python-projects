import matplotlib.pyplot as plt
import pandas as pd

class Chart(object):
    def __init__(self, path_to_file, region, chart_type):
        self.path_to_file = path_to_file
        self.file = path_to_file + '/' + region + '.csv'
        self.region = region
        self.chart_type = chart_type
        self.df = pd.read_csv(self.file)

    def set_chart(self, data):
        medal_data = self.df[data].value_counts().plot(kind=self.chart_type)

    def set_title(self, title):
        plt.title(title)

    def plot_chart(self):
        plt.savefig(self.path_to_file + '/' + self.region)
