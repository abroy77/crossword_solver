import json
import requests
import os
import openai
from dataclasses import dataclass
from typing import List
from clues.parse_clues import read_clues
from config import Config
import random
# read api ley from environment


@dataclass
class Query():

    @dataclass
    class Inputs():
        source_sentence: str
        sentences: list

        def __init__(self, source_sentence: str, sentences: List[str]) -> None:
            self.source_sentence = source_sentence
            self.sentences = sentences
            return

    inputs: Inputs

    def __init__(self, source_sentence: str, sentences: List[str]) -> None:
        self.inputs = self.Inputs(source_sentence, sentences)

    def __repr__(self) -> str:
        return f'Query({self.inputs.source_sentence}, {self.inputs.sentences})'

    def to_dict(self) -> dict:
        query_dict = {
            "inputs": {
                "source_sentence": self.inputs.source_sentence,
                "sentences": self.inputs.sentences
            }
        }
        return query_dict


class SimilarityGenerator():

    def __init__(self) -> None:

        self.api_token = os.environ.get("HUGGINGFACE_TOKEN")
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        self.similarity_model = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        return

    def generate(self, query: Query) -> List[float]:
        query_dict = query.to_dict()
        response = requests.post(self.similarity_model, headers=self.headers, json=query_dict)
        return response.json()


def test():
    query = Query("That is a happy person", [
        "That is a happy dog",
        "That is a very happy person",
        "Today is a sunny day"
    ])
    similarity_generator = SimilarityGenerator()
    response = similarity_generator.generate(query)

    return response


def test_clues():
    clues = read_clues(Config.mini_clues_path)
    print(clues.head())
    clue = str(clues['clue'].sample(1, random_state=42).iloc[0])
    answers = list(clues['answer'])
    query = Query(clue, answers)
    similarity_generator = SimilarityGenerator()
    response = similarity_generator.generate(query)
    return response


def main():
    test_clues()
    return


if __name__ == "__main__":
    main()
