from io import TextIOWrapper
# pip install pandas
import pandas as pd


class MyReport:

    def __init__(self, file: str):
        self.file = file

    def write_file(self, list_items: list, header: str = ""):
        new_file: TextIOWrapper = open(self.file, "w")
        new_file.write(header + "\n")
        for item in list_items:
            new_file.write(str(item).removeprefix(
                "[").removesuffix("]") + "\n")
        new_file.close()

    def get_head_register_csv(self, number: int = None):
        if(number is None):
            return self._read_file().head()
        else:
            return self._read_file().head(n=number)

    def get_tail_register_csv(self, number: int = None):
        if(number is None):
            return self._read_file().tail()
        else:
            return self._read_file().tail(n=number)

    def get_value_counts(self, column_name: str):
        return self._read_file()[column_name].value_counts()

    def _read_file(self):
        return pd.read_csv(self.file)
