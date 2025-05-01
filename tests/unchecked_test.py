from wolern.src.unchecked import get_unsorted_list_of_new_words
from wolern.src.utils import STANDART_VOCABULARY_PATH
from wolern.src.vocabulary import get_vocabulary

if __name__ == "__main__":
    print(get_unsorted_list_of_new_words(get_vocabulary(STANDART_VOCABULARY_PATH)))
