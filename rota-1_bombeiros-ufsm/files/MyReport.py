from io import TextIOWrapper
# pip install pandas
import pandas as pd

import matplotlib.pyplot as plt


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

    def get_group_mean(self, column_name: str, secondary_column_name: str = None):
        if (secondary_column_name is None):
            dataset = self._read_file().groupby([column_name])[['people_on_bus']].agg(['mean', 'count']).round(2)
            dataset.plot(kind='bar', x='bus_id', y='people_on_bus', legend=False)
            plt.show()
            return dataset
        else:
            dataset = self._read_file().groupby([column_name])[['people_on_bus']].agg(['mean', 'count']).round(2)
            dataset.plot.bar()
            plt.show()
            return dataset

    def _read_file(self):
        # TODO - implementar o read_file receber o header dinamicamente
        return pd.read_csv(self.file, names=['bus_id', 'people_on_bus', 'step_log'], header=None)
