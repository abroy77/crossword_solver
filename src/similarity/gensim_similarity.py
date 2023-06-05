""" wordnet seems like not the best systen for similarity. simplest is to get a pretrained wod embedding
model and use that. perhaps even sentence embedding.
"""
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import gensim
from nltk.data import find


def get_encoder():
    word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
    model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)
    return model


def main():

    sentence = "barbell metal"
    answer = "iron"
    encoder = get_encoder()

    sentence_tokens = word_tokenize(sentence)
    # remove stopwords
    sentence_tokens = [x for x in sentence_tokens if x not in gensim.parsing.preprocessing.STOPWORDS]

    # get the similarities
    similarities = []
    for token in sentence_tokens:
        similarities.append(encoder.similarity(token, answer))
    print(similarities)

    return


if __name__ == "__main__":
    main()
