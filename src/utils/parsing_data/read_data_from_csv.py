import csv


def make_dict_from_csv(path: str, delimiter: str = ";") -> list[dict]:
    with open(path, encoding="windows-1251") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        return list(reader)
