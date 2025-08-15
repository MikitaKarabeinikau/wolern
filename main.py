import datetime
import time
import logging
from random import randint

import quiz
import utils
from utils import PATH_TO_LOG_FILE

logging.basicConfig(filename=PATH_TO_LOG_FILE, level=logging.INFO)
from src.vocabulary import Vocabulary_Manager, Vocabulary
import pprint


def main():
    manager = Vocabulary_Manager()
    while True:
        command = input(f'Write a command:\n'
                        f'word: get word\n'
                        f'quiz: to open quiz menu\n'
                        f'vocabulary: to open vocabulary menu\n'
                        f'run: to check current function\n'
                        f'test: to generate test set\n'
                        f'quit: to close the app\n')
        if command == 'run':
            def count_data(arr):
                counter = {}
                for i in arr:
                    if i in counter.keys():
                        counter[i] +=1
                    else:
                        counter[i] = 1
                return counter

            #TODO: CHECK d1
            def compare_to_dict(d1,d2):
                if d1.keys() != d2.keys():
                    print(f'Find dif in sets \n'
                          f'1: {set(d1.keys())-set(d2.keys())}\n'
                          f'2: {set(d2.keys())-set(d1.keys())}\n')

                    raise ValueError('keys not the same ')
                difs = {}
                for i in d1.keys():
                    if i in d1.keys() and i in d2.keys():
                        difs[i] = d1[i]-d2[i]
                    elif i not in d1.keys() and i in d2.keys():
                        difs[i] = -d2[i]
                    elif i in d1.keys() and i not in d2.keys():
                        difs[i] = d1[i]

                return difs

            current_goal = 'Generate quiz linked list\n====================\n'
            print(f'Current goal is: {current_goal}')
            #create first element
            arr = []
            for i in range(0,50):
                day = randint(1,29)
                month = randint(1,12)
                year = 2025
                hour = randint(1,23)
                minute = randint(1,59)
                second = randint(1,59)
                date = datetime.datetime(year=year,month=month,day=day,hour=hour,minute=minute,second=second)

                arr.append(date)

            print(f'\n\nOriginal arr: {arr}\n')
            l = quiz.LinkedVocabulary(arr[0])
            len_before_take_init_arg = len(arr)
            arr = arr[1
            if len_before_take_init_arg == len_after_take_init_arg:
                raise IndexError(f'length of array  couldnt be the same {len_before_take_init_arg} == {len_after_take_init_arg}')
            for i in arr:
                l.insert(i)
            print(f'Counter of initial arr: {count_data(arr)}\n'
                  f'Counter of linked data: {count_data(l.print_all())}\n')
                  # f'Differens between them: {compare_to_dict(count_data(arr),count_data(l.print_all()))}')
            print(f'Inintial arr: {arr}')
            print(f'Final result: {len(arr)} == {len(l.print_all())}')
            #print
        elif command == 'test':
            test_words = utils.get_words_from_translation_cache()
            manager.create_empty_json_file('test')
            manager.load_all_vocabularies()
            for word in test_words:
                print(f'Looking info for word {word.upper()}')
                manager.collection['test'].add_word_to_vocabulary(word)
                time.sleep(10)
        elif command == 'quiz':
            while True:
                quiz_command = input(f'Write command to:\n'
                                     f'time: to get time to repeat\n'
                                     f'five_random: to test changing time\n'
                                     f'\n'
                                     f'back: to back in previous menu\n'
                                     f'quit: to close app\n')
                if quiz_command == 'time':
                    quiz.get_learning_words_with_date_to_repeate()
                elif quiz_command == 'five_random':
                    quiz.change_five_random_data()
                elif quiz_command == 'back':
                    break
                elif quiz_command == 'quit':
                    exit()
        elif command == 'vocabulary':
            while True:
                vocabulary_command = input(f'Write command to:\n'
                                           f'list: get list of dictionary\n'
                                           f'show: show vocabulary\n'
                                           f'open: to open vocabulary\n'
                                           f'size: print size of vocabulary\n'
                                           f'back: to return in previous menu\n'
                                           f'quit: to close app\n')
                if vocabulary_command == 'list':
                    print(manager.get_list_of_all_vocabularies())

                elif vocabulary_command == 'open':
                    vocabulary_to_open = input(f'What vocabulary you want to open: {manager.get_list_of_all_vocabularies()}\n')
                    # CHOSEN VOCABULARY MENU
                    while True:
                        print(f'You are in {vocabulary_to_open}\n')
                        into_vocabulary = input(f'What you want to do: \n'
                                                f'add: to add word in vocabulary\n'
                                                f'delete: delete word from vocabulary\n'
                                                f'display: to display words\n'
                                                f'clean: if you want to clean vocabulary\n'
                                                f'back: to back in previous menu\n'
                                                f'quit: to close app\n')
                        if command == 'show':
                            vocabulary = Vocabulary('known')
                            pprint.pprint(vocabulary.vocabulary)
                        elif command == 'clean':
                            vocabulary_name = input('What vocabulary\n')
                            manager.collection[vocabulary_to_open].clean_vocabulary()
                        elif command == 'size':
                            pprint.pprint(Vocabulary('known').get_size())
        elif command == 'word':
            while True:
                word_command = input(f'Write a command:\n'
                                     f'words_in: show list of words\n'
                                     f'definition: if you want to get definition of the word\n'
                                     f'add: add word to vocabulary\n'
                                     f'delete: to delete word from vocabulary\n'
                                     f'example: to show examples\n'
                                     f'update: change word data'
                                     f'back: to change to previously\n'
                                     f'quit: to close app\n')
                if word_command == 'definition':
                    word = input('input word\n')
                    voc = Vocabulary('known')
                    if voc.is_word_in_vocabulary(word): print(voc.get_word_from_vocabulary(word).get_definition())
                elif word_command == 'delete':
                    word = input('input word:\n')
                    if voc.is_word_in_vocabulary(word): Vocabulary('known').delete_word_from_vocabulary(word)
                elif word_command == 'add':
                    word = input('input word:\n')
                    if not Vocabulary('known').is_word_in_vocabulary(word): Vocabulary('known').add_word_to_vocabulary(
                        word)
                elif word_command == 'example':
                    word = input('input word\n')
                    if Vocabulary('known').is_word_in_vocabulary(word):
                        word = Vocabulary('known').get_word_from_vocabulary(word)
                        word.show_examples()
                elif word_command == 'words_in':
                    voc = Vocabulary('known').get_list_of_words()
                    print(voc)
                elif word_command == 'quit':
                    exit()
                elif word_command == 'back':
                    break
                elif word_command == 'update':
                    word = input(f'print word that info you want to change:\n')
                    if Vocabulary('known').is_word_in_vocabulary(word):
                        inputed_word = Vocabulary('known').get_word_from_vocabulary(word)
                        while True:
                            parameter_to_update = input(f'Write a update parameter:\n'
                                                        f'tag : to add tag\n'
                                                        f'back: to go in previous menu\n'
                                                        f'quit: to close app\n')
                            if parameter_to_update == 'tag':
                                tag = input(f'What tag you whant to add\n')
                                inputed_word.add_tags(tag)
                                print(inputed_word)

                                manager.update_all_vocabularies(inputed_word)
                            elif parameter_to_update == 'back':
                                break
                            elif parameter_to_update == 'quit':
                                exit()
                    else:
                        print('Word does not exist in vocabulary\n'.upper())
        elif command == 'quit':
            pprint.pprint(f'See later!')
            break
        else:
            pprint.pprint(f'wrong command. try again'.upper())


if __name__ == "__main__":
    main()
