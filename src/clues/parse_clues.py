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
    ext = path.splitext(filepath)[1]
    if ext == '.csv':
        df = pd.read_csv(filepath)
    elif ext == '.parquet':
        df = pd.read_parquet(filepath)
    return df


def make_mini_clues(input_file: str, output_file: str, num_clues: int) -> None:
    clues = read_clues(input_file)
    clues = clues.sample(num_clues)
    ext = path.splitext(output_file)[1]
    if ext == '.csv':
        clues.to_csv(output_file)
    elif ext == '.parquet':
        clues.to_parquet(output_file)
    return


def clue_search(clues_df: pd.DataFrame, clue: str, length: int = None) -> str:
    # search for the clue in the 'clues' column of the dataframe
    if length:
        clues_df = clues_df[clues_df['length'] == length]
    results = clues_df[clues_df['clue'].str.contains(clue)]
    if len(results) == 0:
        return None
    else:
        return list(results['answer'])


def test_clue_search(clues_file: str, clue: str, length: int = None) -> None:
    clues_df = read_clues(clues_file)
    answer = clue_search(clues_df, clue, length)
    if answer:
        print(answer)
    else:
        print("No answer found")
    return


def main():
    # clean_clues(Config.clues_path)
    # clues = read_clues(Config.cleaned_clues_path)
    # make_mini_clues(Config.cleaned_clues_path, Config.mini_clues_path, 10000)
    test_clue_search(Config.cleaned_clues_path, "pet rodent", length=7)

    return


if __name__ == "__main__":

    main()
