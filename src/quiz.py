from random import randint

from vocabulary import Vocabulary
from word import Word


class LinkedVocabulary:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        # print(f'{self.data} was created\n====================\n')

    def __str__(self):
        return f'self: {self.data}\n\tleft: {self.left.data}\n\tright: {self.right.data}\n\n'

    def add_to_left(self, data):
        self.left = LinkedVocabulary(data, left=self.left, right=self)
        # print(f'Word {data} was add to the left\n\n')

    def add_to_right(self, data):
        self.right = LinkedVocabulary(data, left=self, right=self.right)
        # print(f'Word {data} was add to the right\n\n')

    def its_first(self, data):
        if self.data > data and self.left is None:
            return True
        return False

    def its_last(self, data):
        if self.data < data and self.right is None:
            return True
        return False

    def its_begin(self):
        if self.left is None:
            return True
        return False

    def its_end(self):
        if self.right is None:
            return True
        return False
    def insert(self, data):
        if self.its_first(data):
            self.add_to_left(data)
        elif self.its_last(data):
            self.add_to_right(data)
        elif self.data > data > self.left.data:
            self.add_to_left(data)
        elif self.data < data < self.right.data:
            self.add_to_right(data)
        elif self.data < data and data > self.right.data:
            self.right.insert(data)
        elif self.data > data and self.left and data < self.left.data:
            self.left.insert(data)
        elif self.data == data:
            self.add_to_right(data)
        elif self.left is not None and data == self.left.data:
            self.left.add_to_right(data)
        elif self.right is not None and self.right.data == data:
            self.right.add_to_right(data)

    def move_to_begin(self):
        current_node = self
        while current_node.left is not None:
            current_node = current_node.left
        return current_node

    def move_to_end(self):
        current_node = self
        while current_node.right is not None:
            current_node = current_node.right
        return current_node


    def print_all(self):

        current_node = self.move_to_begin()
        text = [current_node.data]
        while current_node.its_end() is False:
            current_node = current_node.right
            text.append(current_node.data)
        print(text)
        return text

def learn_words():
    pass


def get_learning_words_with_date_to_repeate():
    learning_vocabulary = Vocabulary('learning').vocabulary
    date_to_repeat = {}
    for word in learning_vocabulary.keys():
        word, time = learning_vocabulary[word]['word'], learning_vocabulary[word]['time_to_repeat']
        date_to_repeat[word] = time
    return date_to_repeat


def change_five_random_data():
    learning_vocabulary = Vocabulary('learning').vocabulary
    words_index = []
    num_of_words = 0

    while num_of_words < 5:
        index = randint(0, len(learning_vocabulary.keys()))
        if index not in words_index:
            words_index.append(index)
            num_of_words += 1
    words = get_learning_words_with_date_to_repeate()
    for index in words_index:
        word_to_change = list(words.keys())[index]
        print(
            f'Word to change before changing time: {word_to_change} \t==\t {learning_vocabulary[word_to_change]["time_to_repeat"]}\n')
        word_data = Vocabulary('learning').vocabulary[word_to_change]
        word_obj = Word(word_data)
        word_obj.change_time_to_repeat(25)
        print(word_obj.time_to_repeat)
        learning_vocabulary[word_to_change]['time_to_repeate'] = word_obj.time_to_repeat
        print(
            f'Word to change after changing time: {word_to_change} \t==\t {learning_vocabulary[word_to_change]["time_to_repeat"]}\n')
        learning_vocabulary.saves()
        print(f'AFTER SAVE CHECK DATE : {Vocabulary("learning").vocabulary[word_obj.word]["time_to_repeat"]}')
