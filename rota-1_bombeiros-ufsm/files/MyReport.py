# pip install pandas
import pandas as pd


class MyReport:

    def __init__(self, file: str):
        self.file = file

    def write_file(self, list_items: list, header: str = ''):
        new_file = open(self.file, "w")
        new_file.write(header + "\n")
        for i in list_items:
            new_file.write(str(i).removeprefix("[").removesuffix("]") + "\n")
        new_file.close()

    def _read_file(self):
        return pd.read_csv(self.file)

    def get_head_register_csv(self, number=50):
        return self._read_file().head(n=number)

    def get_tail_register_csv(self, number=50):
        return self._read_file().tail(n=number)
