from io import TextIOWrapper
import dis
# pip install pandas
import pandas as pd

import matplotlib.pyplot as plt
from datetime import datetime


class MyReport:

    def __init__(self, file: str):
        self.file = file

    def write_file(self, list_items: list):
        new_file: TextIOWrapper = open(self.file, "w")
        for item in list_items:
            # TODO evitar ter que fazer esse tipo de tratamento, linha já poderia vir sem
            new_file.write(str(item).replace("(", "").replace(")", "") + "\n")
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

    def get_group_mean(self, column_name: str, print_log: bool = False, show_plot: bool = False, create_file: bool = False):
        dataset = self._read_file().groupby([column_name])[
            ['people_on_bus']].mean().round(2)

        if(print_log):
            print(dataset)

        if(create_file):
            self.create_file(dataset, self.get_group_mean.__name__)

        if(show_plot):
            dataset.plot.bar()
            plt.show(block=False)

    # def get_group_mean_multi_columns(self, *columns_name: str, print_log: bool = False, show_plot: bool = False, create_file: bool = False):
    #     dataset = self._read_file().groupby(columns_name).mean().round(2)
    #     dataset.plot.pie(y='people_on_bus', figsize=(
    #         5, 5), autopct='%1.1f%%', shadow=True, startangle=90)
    #     plt.show()
    #     return dataset

    def _read_file(self):
        # TODO - implementar o read_file receber o header dinamicamente
        return pd.read_csv(self.file, names=['bus_id', 'people_on_bus', 'step_log'], header=None)

    def create_file(self, dataset, name_file):
         
        df = pd.DataFrame(dataset)
        df.to_csv("dist/" + name_file + '_' + self._get_now() +
                  '.csv', index=True, header=True)

    def _get_now(self):
        return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")