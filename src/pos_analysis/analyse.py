from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk
from clues.parse_clues import read_clues
from config import Config
from os import path
from tqdm import tqdm
from multiprocessing import Pool
from typing import Dict


def ne_regonizer(text):
    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    chunked = ne_chunk(tags, binary=False)

    return chunked


def process_row(in_row_tuple):
    _, row = in_row_tuple
    clue = row['clue']
    answer = row['answer']
    # tokenize the clue
    tokenized_clue = word_tokenize(clue)
    # get the tags
    clue_tags = pos_tag(tokenized_clue)
    answer_tag = pos_tag([answer])[0][1]
    clue_parts = [x[1] for x in clue_tags]
    clue_parts_str = (' ').join(clue_parts)
    return (clue_parts_str, answer_tag)


def pos_tag_clues(input_file: str, output_file: str):

    tags = []
    answer_tags = []
    clues = read_clues(input_file)
    with Pool() as p:

        results = p.map(process_row, clues.iterrows())

    for result in results:
        tags.append(result[0])
        answer_tags.append(result[1])

    clues['clue_tags'] = tags
    clues['answer_tag'] = answer_tags

    ext = path.splitext(output_file)[1]
    if ext == '.csv':
        clues.to_csv(output_file)
    elif ext == '.parquet':
        clues.to_parquet(output_file)
    return


# TODO make a POS predicter that predicts the POS of the answer given the clue.
# may need to look at training an actual classifier. maybe using an existing model of sorts. idk.


def main():
    # pos_tag_clues(Config.cleaned_clues_path, Config.clues_with_tag)
    pos_tag_clues(Config.mini_clues_path, Config.mini_clues_with_tag)
    # chunks = ne_regonizer("Jane Austen is an author. Random House is not")
    # for index, chunk in enumerate(chunks):
    #     print(index, chunk)

    return


if __name__ == "__main__":
    main()
