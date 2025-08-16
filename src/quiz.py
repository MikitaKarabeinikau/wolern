from random import randint

import fetchers
from vocabulary import Vocabulary
from word import Word


class LinkedVocabulary:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        # print(f'{self.data} was created\n====================\n')
    def __iter__(self):
        """
        Returns the iterator object (self) and initializes the current position.
        """
        self.current = self.move_to_begin()  # Start the iteration from the first node
        return self

    def __next__(self):
        """
        Returns the next item in the sequence.
        """
        if self.current is None:
            raise StopIteration
        else:
            # Store the current node to be returned
            node_to_return = self.current
            # Move to the next node for the next call
            self.current = self.current.right
            # Return the node
            return node_to_return
    def __str__(self):
        return f'=================================================================\n' \
               f'Word: {self.data["word"]}\t\tTime to repeat: {self.data["time_to_repeat"]}\t\tAdded: {self.data["date_added"]}\n' \
               f'________________________________________________________________________\n' \
               f'Definition:\n' \
               f'\t{"".join(fetchers.hide_similar_parts(self.data["word"],self.data["definition"]))}\n' \
               f'Translation:\n' \
               f'\t     \n' \
               f'====================================================================='
    def add_to_left(self, data):
        self.left = LinkedVocabulary(data, left=self.left, right=self)
        # print(f'Word {data} was add to the left\n\n')

    def add_to_right(self, data):
        self.right = LinkedVocabulary(data, left=self, right=self.right)
        # print(f'Word {data} was add to the right\n\n')

    def its_first(self, data):
        if self.data['time_to_repeat'] > data['time_to_repeat'] and self.left is None:
            return True
        return False

    def its_last(self, data):
        if self.data['time_to_repeat'] < data['time_to_repeat'] and self.right is None:
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
        new_node = LinkedVocabulary(data)

        if self.its_first(data):
            self.add_to_left(data)
        elif self.its_last(data):
            self.add_to_right(data)
        elif self.data['time_to_repeat'] >= data['time_to_repeat'] >= self.left.data['time_to_repeat']:
            self.add_to_left(data)
        elif self.data['time_to_repeat'] <= data['time_to_repeat'] <= self.right.data['time_to_repeat']:
            self.add_to_right(data)

        elif self.data['time_to_repeat'] < data['time_to_repeat'] and data['time_to_repeat'] > self.right.data['time_to_repeat']:
            self.right.insert(data)
        elif self.data['time_to_repeat'] > data['time_to_repeat'] and self.left and data['time_to_repeat'] < self.left.data['time_to_repeat']:
            self.left.insert(data)

        # CASE : ONE OF SIDE IS EMPTY
        elif self.left is not None and data['time_to_repeat'] >= self.left.data['time_to_repeat']:
            self.left = new_node
        elif self.right is not None and self.right.data['time_to_repeat'] <= data['time_to_repeat']:
            self.right = new_node

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

