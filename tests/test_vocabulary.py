from wolern.src.utils import STANDART_UNCHECKED_PATH, STANDART_VOCABULARY_PATH
from wolern.src.vocabulary import add_word_to_vocabulary, show_vocabulary, get_vocabulary, get_list_of_words, \
    show_all_vocabularies, get_list_of_new_words, pop_word_from_vocabulary, get_unchecked_words_list
from wolern.src.word import Word

if __name__ == '__main__':
    # print(show_vocabulary_list(get_vocabulary()))
    print(get_unchecked_words_list())