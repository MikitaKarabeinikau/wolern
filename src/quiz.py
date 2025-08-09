from random import randint

from vocabulary import Vocabulary
from word import Word


def learn_words():
    pass


def get_learning_words_with_date_to_repeate():
    learning_vocabulary = Vocabulary('learning').vocabulary
    date_to_repeat = {}
    for word in learning_vocabulary.keys():
        word,time = learning_vocabulary[word]['word'],learning_vocabulary[word]['time_to_repeat']
        date_to_repeat[word] = time
    return date_to_repeat

def change_five_random_data():
    learning_vocabulary = Vocabulary('learning').vocabulary
    words_index = []
    num_of_words = 0

    while num_of_words < 5:
        index = randint(0,len(learning_vocabulary.keys()))
        if index not in words_index:
            words_index.append(index)
            num_of_words+=1
    words = get_learning_words_with_date_to_repeate()
    for index in words_index:
        word_to_change = list(words.keys())[index]
        print(f'Word to change before changing time: {word_to_change} \t==\t {learning_vocabulary[word_to_change]["time_to_repeat"]}\n')
        word_data = Vocabulary('learning').vocabulary[word_to_change]
        word_obj = Word(word_data)
        word_obj.change_time_to_repeat(5)
        learning_vocabulary[word_to_change] = word_obj.to_dict()
        Vocabulary('learning').save()
        print(f'Word to change after changing time: {word_to_change} \t==\t {learning_vocabulary[word_to_change]["time_to_repeat"]}\n')

        learning_vocabulary[word_to_change] = word_obj.to_dict()
        Vocabulary('learning').save()



