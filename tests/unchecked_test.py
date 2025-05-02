from wolern.src.unchecked import get_unsorted_list_of_new_words, sort_unchecked_by_frequency
from wolern.src.utils import STANDART_VOCABULARY_PATH
from wolern.src.vocabulary import get_vocabulary

if __name__ == "__main__":
    sorted_list = sort_unchecked_by_frequency(get_vocabulary(STANDART_VOCABULARY_PATH))
    sorted_list.pop()
