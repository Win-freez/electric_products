import csv
from pprint import pprint


def make_dict_from_csv(path: str, delimiter=';') -> list[dict]:
    with open(path, 'rt') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        return list(reader)

pprint(make_dict_from_csv(r'C:\Users\tdrubin.com\Downloads\цены электрика.csv'))