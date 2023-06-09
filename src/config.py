from dataclasses import dataclass


@dataclass
class Config():
    clues_path = "/Users/abhishekroy/code/local_data/personal/clues"
    cleaned_clues_path = "/Users/abhishekroy/code/local_data/personal/clues_cleaned.parquet"
    mini_clues_path = "/Users/abhishekroy/code/local_data/personal/mini_clues.parquet"
    mini_clues_with_tag = "/Users/abhishekroy/code/local_data/personal/mini_clues_tagged.csv"
    clues_with_tag = "/Users/abhishekroy/code/local_data/personal/clues_tagged.parquet"
    puzzles_dir = "/Users/abhishekroy/code/crossword_solver/puzzles"
