from io import TextIOWrapper
# pip install pandas
import pandas as pd

import matplotlib.pyplot as plt
from datetime import datetime
from itertools import cycle, islice


class MyReport:

    def __init__(self,  header_name_columns: list):
        self.file = "dist/" + self.__class__.__name__ + '_' + self._get_now() + '.csv'
        self.header_name_columns = header_name_columns

    def write_file(self, list_items: list):
        new_file: TextIOWrapper = open(self.file, "w")
        for item in list_items:
            # TODO evitar ter que fazer esse tipo de tratamento, linha já poderia vir sem
            new_file.write(str(item) + "\n")
        new_file.close()

    def get_head_register_csv(self, number: int = 5):
        return self._read_file().head(n=number).to_string()

    def get_tail_register_csv(self, number: int = 5):
        return self._read_file().tail(n=number).to_string()

    def get_value_counts(self, column_name: str):
        return self._read_file()[column_name].value_counts()

    def get_shape(self):
        return self._read_file().shape

    def get_info(self):
        return self._read_file().info()

    def get_describe(self):
        return self._read_file().describe()

    def extract_information(self, columns_to_group_by,
                            columns_to_select_by, functions_name_pandas,
                            print_log: bool = False, show_plot: bool = False,
                            create_file: bool = False,
                            kind_plot_name: str = 'bar'
                            ):

        dataset = self._read_file().groupby(columns_to_group_by)[
            columns_to_select_by].agg(functions_name_pandas).reset_index().round(2)

        if(print_log):
            print(dataset)

        if(create_file):
            self._create_file(dataset, self.extract_information.__name__)

        if(show_plot):
            # TODO color
            my_colors = list(
                islice(cycle(['b', 'r', 'g', 'y', 'k']), None, len(dataset)))
            self._create_plot(dataset, kind_plot_name, my_colors)

    def _read_file(self):
        return pd.read_csv(self.file, names=self.header_name_columns, header=None)

    def _create_file(self, dataset, name_file):
        df = pd.DataFrame(dataset)
        df.to_csv("dist/" + name_file + '_' + self._get_now() +
                  '.csv', index=True, header=True)

    def _get_now(self):
        return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def _create_plot(self, dataset, kind_plot_name, my_colors):

        dataset.plot(kind=kind_plot_name,  color=my_colors)
        plt.ion()
        plt.show()
        plt.draw()
        plt.pause(0.001)
        input("Press Enter to continue...")
