from nltk.tokenize import word_tokenize
from nltk import pos_tag
from clues.parse_clues import read_clues
from config import Config
from os import path


def pos_tag_clues():

    tags = []
    answer_tags = []
    clues = read_clues(Config.mini_clues_path)
    for _, row in clues.iterrows():
        clue = row['clue']
        answer = row['answer']
        # tokenize the clue
        tokenized_clue = word_tokenize(clue)
        # get the tags
        clue_tags = pos_tag(tokenized_clue)
        answer_tag = pos_tag([answer])[0][1]
        clue_parts = [x[1] for x in clue_tags]
        clue_parts_str = (' ').join(clue_parts)
        tags.append(clue_parts_str)
        answer_tags.append(answer_tag)

    clues['clue_tags'] = tags
    clues['answer_tag'] = answer_tags
    savefile = path.join(path.dirname(Config.mini_clues_path), 'mini_clues_tagged.csv')
    clues.to_csv(savefile)


# TODO make a POS predicter that predicts the POS of the answer given the clue.
# may need to look at training an actual classifier. maybe using an existing model of sorts. idk.


def main():
    pos_tag_clues()
    return


if __name__ == "__main__":
    main()
