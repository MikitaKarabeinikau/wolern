import json
import os.path
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "backend", "src"))

from random import randint

import fetchers
import utils
from utils import PATH_TO_LEARNING_CACHE
from vocabulary import Vocabulary, Vocabulary_Manager
from word import Word

manager = Vocabulary_Manager()
if not os.path.exists(PATH_TO_LEARNING_CACHE):
    cache = {}
else:
    cache = json.loads(PATH_TO_LEARNING_CACHE.read_text(encoding='utf-8'))


class LinkedVocabulary:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

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

    def __repr__(self):
        return f'=================================================================\n' \
               f'Word: {self.data["word"]}\t\tTime to repeat: {self.data["time_to_repeat"]}\t\tAdded: {self.data["date_added"]}\n' \
               f'________________________________________________________________________\n' \
               f'Definition:\n' \
               f'\t{"".join(fetchers.hide_similar_parts(self.data["word"], self.data["definition"]))}\n' \
               f'Translation:\n' \
               f'\t     \n' \
               f'====================================================================='

    def add_to_left(self, data):
        self.left = LinkedVocabulary(data, left=self.left, right=self)

    def add_to_right(self, data):
        self.right = LinkedVocabulary(data, left=self, right=self.right)

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

        elif self.data['time_to_repeat'] < data['time_to_repeat'] and data['time_to_repeat'] > self.right.data[
            'time_to_repeat']:
            self.right.insert(data)
        elif self.data['time_to_repeat'] > data['time_to_repeat'] and self.left and data['time_to_repeat'] < \
                self.left.data['time_to_repeat']:
            self.left.insert(data)

        # CASE : ONE OF SIDE IS EMPTY
        elif self.left is not None and data['time_to_repeat'] >= self.left.data['time_to_repeat']:
            self.left = new_node
        elif self.right is not None and self.right.data['time_to_repeat'] <= data['time_to_repeat']:
            self.right = new_node

    def formate_definition_to_display(self):
        definition = self.data['definition']
        formatted_definition = ""
        for pos in definition.keys():
            formatted_definition += f'{pos}:\n'
            for index, df in enumerate(definition[pos]):
                splited = df.split()
                for word in range(0, len(splited)):
                    splited[word] = fetchers.hide_similar_parts(self.data['word'], splited[word])
                    splited[word] = ''.join(splited[word])

                df = ' '.join(splited)

                formatted_definition += f'\t{index}: {df}\n'
        return formatted_definition

    def formate_examples_to_display(self):
        examples = self.data['examples']
        formatted = 'Examples:\n'
        for index, example in enumerate(examples):
            formatted += f'\t{index}: {fetchers.hide_similar_parts(self.data["word"], example)}\n'
        return examples

    def formate_synonyms_to_display(self):
        formatted = []
        for word in self.data['synonyms']:
            formatted.append(fetchers.hide_similar_parts(self.data['word'], word))
        return formatted

    def display_learning_info(self):
        self.data['word']['last_reviewed'] = utils.current_datetime()
        result = []
        definition = self.formate_definition_to_display()
        examples = self.formate_definition_to_display()
        synonyms = self.formate_synonyms_to_display()

        translation = self.data['translation']
        formatted_translation = ''
        for lang, trans in translation.items():
            part = f'Language: {lang.upper()}\n'
            if trans is not None:

                translation_sentence = '\t'.join(trans)
                formatted_translation += part + translation_sentence
            else:
                formatted_translation += '\n'
        # Add element one by one
        result.append(
            f'Word: ... \tPart of speech: {" ".join(self.data["part_of_speech"])}\tFrequency: {self.data["frequency"]}\n')
        result.append(f'Definition:\n{definition}\n')
        result.append(f'Examples:\n{examples}\n')
        result.append(f'Synonyms:\n\t{" ".join(synonyms)}\n')
        result.append(f'Translation:\t {formatted_translation}')
        return ''.join(result)

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

    def set_new_time_for_repeat(self, mistake):
        word = self.data['word']
        print(f'Word: {word}\n')
        count_of_wrong_answers = 0 if cache[word] not in cache.keys() else cache[word]['count_of_wrong_answers']
        print(f'Count of wrong answers :{count_of_wrong_answers} | Courant mistakes: {mistake}\n')
        # IF perfect answer than change learning stage or reset count_of_wrong_answer
        if mistake == 0 and self.data['learning_stage'] == 4 and count_of_wrong_answers == 0:
            archive_to_known(self.data)
        elif mistake == 0:
            cache[word]['count_of_wrong_answers'] = 0

        '''
        If not perfect answer:
            depends on counter_of_wrongs_ansers set new time to repeat 
        
        1. update data in cache 
            A question arises, do i want to update my vocabularies already in place or from cache before exit() 
                or do it both
        2. update data in vocabulary from manager 
        
        '''
        count_of_wrong_answers = cache['word']['count_of_wrong_answers'] if word in cache.keys() else 0

        interval = time_range(self.data)
        cache[self.data.word]['time_to_repeat'] = utils.change_repeat_time(interval)


def save_cache():
    with open(PATH_TO_LEARNING_CACHE, 'w', encoding='utf-8') as f:
        json.dump(cache, indent=2, ensure_ascii=False)


def normalize_lengths_and_calculate_mistakes(answer, word):
    if len(answer) < len(word):
        for i in range(len(word) - len(answer)):
            answer.append('*')
        return calculate_mistakes(word, answer)
    elif len(answer) > len(word):
        word = [i for i in word]
        for i in range(len(answer) - len(word)):
            word.append('*')
        return calculate_mistakes(word, answer)


def check_sync_cache_with_vocabulary():
    '''
    check data synchronization cache with vocabulary
    based on time review
    if cache data is later
    then change vocabulary data
    save it
    :return: True
    '''
    pass


'''
1. Check sync with cache
2. Get linked vocabulary
3. get input
4. check answer -> percentage of wronge answer
    
    is perfect (100%)-> increase learning stage / reset counter 
        perfect and stage == 4 and counter == 0 -> change vocabulary -> update cache -> save vocabulary
    good (<= 80%) -> reset counter -> update cache 
    bad (>80%) -> counter ++ -> update cache 
5. set time to reapet
    get interval 
    set 
    cache update
    cahce save
    add new LinkedNode to LinkedVocabulary  
6. linkedVocabulary.insert(current_updated_node)

'''


def calculate_accuracy(mistakes, word):
    # 6 letter / 100
    # 4 letters / x
    # 4* 100 / 6 = 30
    return float("%.2f" % (1 - (mistakes * 100 / len(word))))


def is_answer_correct(accuracy):
    return False if accuracy < 80 else True


def increase_count_of_wrong_answers(word):
    if cache[word]['count_of_wrong_answers'] + 1 == 10 and word in cache.keys():
        # I need to be sure that word record exist in
        if cache[word]['learning_stage'] > 0:
            cache[word]['learning_stage'] -= 1
            cache[word]['count_of_wrong_answers'] = 0
    else:
        cache[word]['count_of_wrong_answers'] += 1

    # save changes

    save_cache()


def calculate_mistakes(answer, word):
    count_of_incorrect_letters = 0
    if len(answer) == len(word):
        for i in range(0, len(word)):
            if word[i] != answer[i]:
                count_of_incorrect_letters += 1
        return count_of_incorrect_letters


def display_differences(answer, word):
    comparing = []
    if len(answer) == len(word):
        for i in range(0, len(word)):
            if word[i] == answer[i]:
                comparing.append('_')
                answer[i] = '_'
            else:
                comparing.append(word[i])
        print(f'Info: \n'
              f'\tOriginal:    {" ".join(word)}\n'
              f'\tAnswer:      {" ".join(answer)}\n'
              f'\tDifferences: {" ".join(comparing)}\n'
              f'\tNumber of wrong letters: {calculate_mistakes(answer, word)}\n')


def learn_stage_conversation_in_time(stage):
    if stage == 0:
        return 5
    elif stage == 1:
        return 15
    elif stage == 2:
        return 60
    elif stage == 3:
        return 60 * 24
    elif stage == 4:
        return 60 * 24 * 7


def calculate_time_to_repeat_based_on_count_of_wrong_answers(data, current_time):
    counter = cache['word']['count_of_wrong_answers']
    if current_time >= 60:
        decrease_review_interval = current_time - ((counter / 10) * current_time)
        print(f'Time to repeat was decreased from {current_time} to {decrease_review_interval}')
        return decrease_review_interval


def time_range(data):
    # Get new time by learning stage
    learn_stage = learn_stage_conversation_in_time(int(data['learning_stage']))
    print(f'Minutes to add after learning stage')
    interval = calculate_time_to_repeat_based_on_count_of_wrong_answers(learn_stage)

    return interval


def archive_to_known(data):
    word = data['word']
    data[word]['learning_stage'] = 5
    cache[word]['learning_stage']
    print(
        f'Moving word from learning to known: \n Word {word} in learning {manager.collection["learning"].is_word_in_vocabulary(word)}\n')
    manager.collection['learning'].delete_word_from_vocabulary(word)
    print(
        f'Moving word from learning to known: \n Word {word} in learning {manager.collection["learning"].is_word_in_vocabulary(word)}\n')
    manager.collection['known'][word] = data
    manager.collection['learning'].save()
    manager.collection['known'].save()
    Vocabulary('known').is_word_in_vocabulary()


def sync_cache_to_vocabulary():
    for word, data in cache.items():
        if data['last_reviewed'] > manager.collection['learning'].vocabulary['last_reviewed']:
            manager.collection['learning'].vocabulary['learning_stage'] = data['learning_stage']
            manager.collection['learning'].vocabulary['last_reviewed'] = data['last_reviewed']
    manager.collection['learning'].vocabulary.save()


def get_valid_answer(prompt):
    while True:
        user_input = input(prompt)
        if user_input is not None and user_input.strip() != "":
            return user_input
        print("Invalid input. Please try again.")


def get_answer():
    answer = get_valid_answer(f'Write your answer: \n')
    return answer


def display_info_about_answer(answer, word):
    if answer == 'qq':
        save_cache()
        sync_cache_to_vocabulary()
        exit()

    answer = [i for i in answer.strip().upper()]
    word = [i for i in word.strip().upper()]

    if len(answer) != len(word):
        return normalize_lengths_and_calculate_mistakes(word, answer)

    return calculate_mistakes(word, answer)


def is_answer_perfect(accuracy):
    return True if accuracy == 100 else False


# TODO:FINISH IT
def check_answer(answer, word):
    accuracy = calculate_accuracy()
    number_of_mistake = calculate_mistakes(answer, word)
    accuracy = calculate_accuracy(number_of_mistake, word)
    if is_answer_correct(accuracy):
        if is_answer_perfect(accuracy):
            if cache[word] + 1 == 5:
                archive_to_known()
    else:
        pass


def get_learning_words_with_date_to_repeat():
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
    words = get_learning_words_with_date_to_repeat()
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
