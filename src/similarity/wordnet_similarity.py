from nltk.corpus import wordnet as wn


def main():
    word = 'chicken'

    synsets = wn.synsets(word)
    print(synsets)
    return


if __name__ == "__main__":
    main()
