import datetime
import logging
import os

from src.sound_manager import generate_audio, get_audio_path

from src.utils import current_datetime, parse_time_to_str, initial_repeat_time, STANDART_VOCABULARY_PATH, \
    STANDART_UNCHECKED_PATH, VOCABULARY_DIR_PATH, STANDART_VOCABULARIES_SET, DEFUALT_USER, PATH_TO_LOG_FILE, \
    delete_audio
from src.fetchers import *
from word import Word

CEFR_CACHE_PATH = Path(__file__).resolve().parent.parent / "data" / "cache" / "cefr_cache.json"
_cache_unchecked_words = json.loads(STANDART_UNCHECKED_PATH.read_text(encoding='utf-8'))

logging.basicConfig(filename=PATH_TO_LOG_FILE)


class Vocabulary_Manager():
    def __init__(self, owner=DEFUALT_USER):
        self.owner = owner
        self.dir = Path(__file__).resolve().parent.parent / 'data' / 'vocabularies' / self.owner
        self.write_standart_vocabularies()
        self.collection = self.load_all_vocabularies()
    def find_word(self, word):
        result = {}
        # go through the vocab
        for vocabulary in self.collection.keys():
            # is word in ?
            if self.collection[vocabulary].is_word_in_vocabulary(word):
                '''
                WHY VOCABULARY HERE IS STR 
                ITS SHOULD BE Vocabulary obj
                '''
                # add info
                result[vocabulary] = self.collection[vocabulary].vocabulary[word]
        # Do I need to check similarity of words or note?
        # Words wouldn't be the identical (added_date)

        return result

    def load_all_vocabularies(self):
        vocabularies = {}
        for voc_name in self.get_list_of_all_vocabularies():
            vocabularies[voc_name[:-5]] = Vocabulary(voc_name[:-5])
        return vocabularies

    def delete_vocabulary(self, vocabulary_name):
        if os.path.isfile(self.dir / (vocabulary_name + '.json')):
            os.remove(self.dir / (vocabulary_name + '.json'))
            print(f'[INFO] {datetime.datetime.now()} Vocabulary {self.dir / (vocabulary_name + ".json")}')
        else:
            raise ValueError(f'Vocabulary {self.dir / (vocabulary_name + ".json")} does not exist')

    def create_empty_json_file(self, vocabulary_name):
        with open(self.dir / (vocabulary_name + ".json"), 'w', encoding='utf-8') as vocabulary:
            json.dump({}, vocabulary, ensure_ascii=False, indent=2)
            print(f'[INFO] {datetime.datetime.now()} Vocabulary {vocabulary_name} was created! {vocabulary}')

    def write_standart_vocabularies(self):
        for vocabulary_name in STANDART_VOCABULARIES_SET:
            if os.path.isfile(self.dir / (vocabulary_name + '.json')) == False:
                self.create_empty_json_file(vocabulary_name)

    def get_list_of_all_vocabularies(self):
        vocabularies = os.listdir(Path(__file__).resolve().parent.parent / "data" / "vocabularies" / self.owner)
        if len(vocabularies) <= 1:
            self.write_standart_vocabularies()
            os.listdir(Path(__file__).resolve().parent.parent / "data" / "vocabularies" / self.owner)
        else:
            return vocabularies

    def is_vocabulary_exit(self, vocabulary_name):
        if vocabulary_name + '.json' in (
                os.listdir(Path(__file__).resolve().parent.parent / "data" / "vocabularies" / self.owner)):
            print(
                f'[INFO] Vocabulary {vocabulary_name} exist in dir : {Path(__file__).resolve().parent.parent / "data" / "vocabularies" / self.owner}')
            return True
        else:
            print(
                f'[INFO] Vocabulary {vocabulary_name} does not exist in dir: {Path(__file__).resolve().parent.parent / "data" / "vocabularies" / self.owner}')
            return False

    def show_all_vocabularies(self):
        if len(self.get_list_of_all_vocabularies()) <= 1:
            self.write_standart_vocabularies()
            return self.get_list_of_all_vocabularies()
        else:
            print(f'List of vocabularies:\n' + '\n'.join(self.get_list_of_all_vocabularies()))
            return self.get_list_of_all_vocabularies()

    def add_new_vocabulary(self, vocabulary_name):
        if self.is_vocabulary_exit(vocabulary_name):
            raise ValueError(f"[ERROR] Vocabulary {vocabulary_name.upper()} is already exist.")
        else:
            self.create_empty_json_file(vocabulary_name)

    def clean_vocabulary(self, vocabulary_name):
        self.create_empty_json_file(vocabulary_name + '.json')

    def update_all_vocabularies(self, updated_word: Word):
        if not isinstance(updated_word, Word):
            raise ValueError("parameter is not a Word class!")
        for vocabulary_name, vocabulary in self.collection.items():
            if vocabulary.is_word_in_vocabulary(updated_word.word):
                vocabulary.vocabulary[updated_word.word] = updated_word.to_dict()
                vocabulary.save()

            # logging.INFO(f'Word : {updated_word.word} was updated in vocabulary {vocabulary_name}')

    def learning_stage_scanner(self):
        '''
        if word learning stage is 5
        than transfer word to known
        remove from current vocabulary
        logging.info(f'Word: {word} was transfer from {old_vocabulary} to known
        :return: Word
        '''
        pass


class Vocabulary():
    def __init__(self, vocabulary_name, owner=DEFUALT_USER):
        self.vocabulary_name = vocabulary_name
        self.owner = owner
        self.dir = self.set_vocabulary_dir()
        self.full_path = self.dir / (self.vocabulary_name + '.json')
        self.vocabulary = self.get_vocabulary()
        self.size = self.get_size()

    def get_size(self):
        return len(self.vocabulary.keys())

    def set_vocabulary_dir(self):
        if os.path.isdir(VOCABULARY_DIR_PATH / self.owner):
            return VOCABULARY_DIR_PATH / self.owner
        else:
            os.mkdir(VOCABULARY_DIR_PATH / self.owner)
            print(f'[INFO] New dir {VOCABULARY_DIR_PATH / self.owner} was created!')
            return VOCABULARY_DIR_PATH / self.owner

    def update_name_of_vocabulary(self, old_name, new_name):
        old_name += '.json'
        self.vocabulary_name = new_name
        new_name = self.dir / (old_name + '.json')
        vocabulary = self.get_vocabulary(old_name)
        self.save()

    def update_vocabulary(self):
        with open(self.full_path, 'w') as file:
            json.dump(self.vocabulary, file, ensure_ascii=False, indent=2)

    def get_vocabulary(self):
        if os.path.isfile(self.full_path):
            return json.loads(self.full_path.read_text(encoding="utf-8"))
        else:
            print(f'[INFO] File {self.full_path} does not exist!\n'
                  f'Opened empty vocabulary.')
            return {}

    def find_warnings(self, word_data):
        warnings = []
        if not word_data.get("translation"):
            warnings.append("Missing translation")
        if not word_data.get("synonyms"):
            warnings.append("No synonyms found")
        if not word_data.get("definition"):
            warnings.append("No definitions available")
        if not word_data.get("examples"):
            warnings.append("No example sentences")
        if not word_data.get("part_of_speech"):
            warnings.append("Missing part of speech")
        if not word_data.get("frequency"):
            warnings.append("Missing frequency")
        if not word_data.get("level"):
            warnings.append("No CEFR level found")
        return warnings

    def add_word_to_vocabulary(self, word):
        print(f'Looking for data ...')
        if word is None:
            raise ValueError(f'Word could not be a None')
        elif len(word) <= 1:
            raise ValueError(f'LENGTH OF WORD COULD NOT BE LESS OR EQUALE 1 ')

        if word in self.vocabulary.keys():
            print(f'Word: {word} already in vocabulary')
            return

        translation = get_translation(word)
        audio_url = generate_audio(word)

        word = {
            "word": word.lower(),
            "translation": get_translation_from_cache(word),
            "synonyms": get_synonyms(word),
            "definition": get_definitions_by_pos(word) if get_definitions_by_pos(word) else [],
            "examples": [get_examples_from_wordnet(word)] if get_examples_from_wordnet(word) else [],
            "part_of_speech": get_parts_of_speech(word),
            "date_added": parse_time_to_str(current_datetime()),
            "last_reviewed": parse_time_to_str(current_datetime()),
            "review_count": 0,
            "learning_stage": 0,
            "time_to_repeat": parse_time_to_str(initial_repeat_time()),
            "notes": "",
            "level": get_cefr_level(word),
            "tags": get_tags_from_wordnet(word) if get_tags_from_wordnet(word) else [],
            "audio_url": str(get_audio_path(word)),
            'frequency': get_frequency(word)
        }

        warnings = self.find_warnings(word)
        word['warnings'] = warnings

        if len(warnings) >= 2:
            weird = Vocabulary('weird')
            weird.vocabulary[word['word']] = word
            weird.save()
        else:
            self.vocabulary[word["word"]] = word
            with (self.dir / (self.vocabulary_name + '.json')).open("w", encoding="utf-8") as f:
                json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)
            print(f"✅ Word '{word}' added to vocabulary.")

    def delete_word_from_vocabulary(self, word):
        if len(self.vocabulary.keys()) == 0:
            logging.error(f'You tried to pop word from empty vocabulary')
            raise IndexError(f'Vocabulary: {self.vocabulary_name} does not contain any words')
        words = self.get_vocabulary()
        deleted_word = Word(word)
        if word in words.keys():
            del words[word]
            delete_audio(word)
            print(f'[INFO] Word: {word.upper()} was deleted from {self.vocabulary_name.upper()}')
            self.save()
            return deleted_word
        else:
            print(f'Word {word.upper()} does not exist in {self.full_path}')

    def move_word_to_weird_vocabulary(self, word):
        word['warnings'] = warnings
        weird_vocabulary = Vocabulary_Manager().collection['weird']
        print(word)
        print(weird_vocabulary.vocabulary_name)
        weird_vocabulary.vocabulary[word['word']] = word
        weird_vocabulary.save()

    def pop_word_from_vocabulary(self):
        deleted_word_data = self.delete_word_from_vocabulary(self.vocabulary.keys()[-1])
        self.save()
        logging.INFO(
            f'Word : {deleted_word_data.word} was poped from {self.vocabulary_name}. Vocabulary was is rewrote.')
        return deleted_word_data

    def is_word_in_vocabulary(self, word):
        if word is None:
            raise ValueError('Word should not be None')
        if len(word) <= 1:
            raise ValueError('Word should have more symbols then 1')
        return True if word in self.vocabulary.keys() else False

    def get_list_of_words(self):
        return list(self.vocabulary.keys())

    def get_word_from_vocabulary(self, word):
        if self.is_word_in_vocabulary(word) == True:
            print(f'Word {word.upper()} exist in {str(self.full_path).upper()}')
            return Word(self.vocabulary[word])
        else:
            print(f'Word {word.upper()} is not in vocabulary {str(self.full_path).upper()}')

    def save(self):
        try:
            data_to_save = self.vocabulary
            with open(self.full_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            print(f'File : {self.full_path} was saved!')
        except IOError as e:
            print(f'{e}')


def get_word_input():
    word = input("Enter the English word").strip().lower()
    return word


def reset_vocabulary_file():
    pass
