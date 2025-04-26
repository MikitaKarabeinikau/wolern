from wolern.src.vocabulary import add_word_to_vocabulary,vocab
from wolern.src.word import Word

if __name__ == '__main__':
    add_word_to_vocabulary('file',vocab)
    f = vocab['file']
    word_f = Word(f)

    word_f.show_word_info()