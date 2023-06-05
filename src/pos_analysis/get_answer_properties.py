""" 
Script to train a classifier to get the POS of the answer given the clue.
"""

import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk
from config import Config
from collections import namedtuple
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from clues.parse_clues import read_clues


MAX_CLUE_LEN = 10

TAGS = ['', 'POS', 'PRP$', 'NNS', 'CD', 'VB', 'NNP', 'CC', 'FW', 'PRP', 'VBG', 'NN', 'WP', 'VBP', 'MD', 'EX', 'UH',
        'RBR', 'WDT', 'TO', 'JJR', 'RP', 'DT', 'IN', 'VBZ', 'VBN', 'JJS', 'VBD', 'RBS', 'PDT', 'WRB', 'RB', 'JJ']

PUNCTUATION = ['.', ',', '/', '\"', '`']

TAGS = TAGS + PUNCTUATION


Data = namedtuple('Data', ['clue_tags', 'answer_tag'])


def get_all_tags(data: list[Data]) -> list[str]:
    all_tags = set()
    for d in data:
        all_tags.add(d.answer_tag)
        all_tags.update(set(d.clue_tags))
    return all_tags


# def naive_classifier(clue_tags: list[str]) -> str:
    # if 'NNS'


def parse_data(filepath: str) -> list[Data]:
    clues = read_clues(filepath)
    data = []
    # filter out fill in the blank clues
    clues = clues[~clues['clue'].str.contains('___')]
    for _, row in clues.iterrows():
        clue_tags = row['clue_tags']
        answer_tag = row['answer_tag']

        clue_tags = list(filter(lambda x: x.isalpha() or x in PUNCTUATION, clue_tags.split()))  # remove punctuation
        # pad the length to MAX_CLUE_LEN
        if len(clue_tags) < MAX_CLUE_LEN:
            clue_tags = clue_tags + [''] * (MAX_CLUE_LEN - len(clue_tags))
        else:
            clue_tags = clue_tags[:MAX_CLUE_LEN]

        data.append(Data(clue_tags, answer_tag))

    return data


def encode_data(data: list[Data], encoder: LabelEncoder) -> list[Data]:

    # encode the data
    new_data = []
    for d in data:
        clue_tags = encoder.transform(d.clue_tags)
        answer_tag = encoder.transform([d.answer_tag])[0]
        new_data.append(Data(clue_tags, answer_tag))

    return new_data


def train_classifier(train: list[Data]) -> DecisionTreeClassifier:

    # train the classifier
    clf = MLPClassifier(activation='relu', hidden_layer_sizes=(100, 100), max_iter=1000, random_state=42)
    train_x = [x.clue_tags for x in train]
    train_y = [x.answer_tag for x in train]
    clf.fit(train_x, train_y)
    return clf


def validate_classifier(clf: DecisionTreeClassifier, data: list[Data]) -> float:
    pred_labels = []
    true_labels = []
    for d in data:
        pred = clf.predict([d.clue_tags])[0]
        pred_labels.append(pred)
        true_labels.append(d.answer_tag)

    return accuracy_score(true_labels, pred_labels)

# def get_punctuation(data: list[Data]) -> list[str]:


def main():
    # read the csv
    data = parse_data(Config.mini_clues_with_tag)
    # get_all_tags(data)
    # encode the data
    encoder = LabelEncoder()
    encoder.fit(TAGS)
    data = encode_data(data, encoder)
    # split into train and test
    train, test = train_test_split(data, test_size=0.2, random_state=42)
    clf = train_classifier(train)
    # validate
    accuracy = validate_classifier(clf, test)
    print(accuracy)

    return


if __name__ == "__main__":
    main()
