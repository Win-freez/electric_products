import csv
from pprint import pprint


def make_dict_from_csv(path: str, delimiter: str = ";") -> list[dict]:
    with open(path) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        return list(reader)


pprint(make_dict_from_csv(r"C:\Users\tdrubin.com\Downloads\цены электрика.csv"))
pprint(make_dict_from_csv(r"C:\Users\tdrubin.com\Downloads\Справочник электрика.csv"))
