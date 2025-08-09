import time
import logging

import quiz
import utils
from utils import PATH_TO_LOG_FILE

logging.basicConfig(filename=PATH_TO_LOG_FILE, level=logging.INFO)
from src.vocabulary import Vocabulary_Manager, Vocabulary
import pprint


def main():
    manager = Vocabulary_Manager()
    while True:
        command = input(f'Write a command:\nc'
                        f'clean: if you want to clean vocabulary\n'
                        f'show : show vocabulary\n'
                        f'word: get word\n'
                        f'quiz: to open quiz menu'
                        f'size: print size of vocabulary\n'
                        f'random: generate random 50 words\n'
                        f'test: generate test vocabulary\n'
                        f'quit: to close the app\n'
                        f'vocabulary: to open vocabulary menu')

        if command == 'clean':
            vocabulary_name = input('What vocabulary\n')
            manager = Vocabulary_Manager()
            manager.clean_vocabulary(vocabulary_name)
        elif command == 'random':
            print(utils.get_N_random_word_from_subtlex_longer_then_3(50))
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
                                        
                                           f'open: to open vocabulary\n'
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
                                                f'back: to back in previous menu\n'
                                                f'quit: to close app\n')

        elif command == 'show':
            vocabulary = Vocabulary('known')
            pprint.pprint(vocabulary.vocabulary)
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
        elif command == 'size':
            pprint.pprint(Vocabulary('known').get_size())
        elif command == 'quit':
            pprint.pprint(f'See later!')
            break
        else:
            pprint.pprint(f'wrong command. try again'.upper())


if __name__ == "__main__":
    main()
