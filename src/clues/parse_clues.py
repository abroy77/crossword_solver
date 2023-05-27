import csv
import pandas as pd
import argparse
from config import Config
from pprint import pprint as print
from collections import namedtuple
from os import path


def clean_clues(filepath: str) -> None:
    with open(filepath, "rb") as f:
        contents = f.read()
    contents = str(contents)
    contents = contents.split("\\n")
    contents[0] = contents[0].split("b'")[1]
    contents = [x.replace('\\', '') for x in contents]
    contents = [(' ').join(x.split()) for x in contents]
    Item = namedtuple('Item', ['clue', 'length', 'answer'])
    items = []
    for line in contents:
        parts = line.split(' ')
        answer = parts[0].lower()
        clue = (' ').join(parts[4:]).lower()
        length = len(answer)

        item = Item(clue, length, answer)
        items.append(item)
    df = pd.DataFrame(items)
    savefile = path.join(path.dirname(filepath), 'clues_cleaned.parquet')
    df.to_parquet(savefile)

    return


def read_clues(filepath: str) -> pd.DataFrame:
    df = pd.read_parquet(filepath)
    return df


def main():
    # clean_clues(Config.clues_path)
    # clues = read_clues(Config.cleaned_clues_path)

    return


if __name__ == "__main__":

    main()
