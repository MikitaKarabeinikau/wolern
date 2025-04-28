from wolern.src.vocabulary import add_word_to_vocabulary, show_vocabulary, get_vocabulary,get_list_of_words , show_all_vocabularies, get_list_of_new_words
from wolern.src.word import Word

if __name__ == '__main__':
    # print(show_vocabulary_list(get_vocabulary()))
    al = get_list_of_words(get_vocabulary())
    un = get_list_of_new_words(get_vocabulary())
    print(f'{al}\n{un}\nDIf:{set(al)-set(un)}')