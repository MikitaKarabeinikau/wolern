import json
import logging
from datetime import timedelta
from pathlib import Path
import utils
from src.sound_manager import get_audio_path

logging.basicConfig(filename=(Path(__file__).resolve().parent.parent / 'logs' / 'app.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Word:
    def __init__(self, word_data):
        self.word = word_data["word"]
        self.translation = word_data["translation"]
        self.synonyms = word_data.get("synonyms", [])
        self.definition = word_data.get("definition", [])
        self.examples = word_data.get("examples", [])
        self.part_of_speech = word_data["part_of_speech"]
        self.date_added = word_data["date_added"]
        self.last_reviewed = word_data["last_reviewed"]
        self._review_count = word_data["review_count"]
        self.learning_stage = word_data["learning_stage"]
        self.time_to_repeat = word_data["time_to_repeat"]
        self.notes = word_data.get("notes", [])
        self.level = word_data.get("level", None)
        self.tags = word_data.get("tags", [])
        self.audio_url = word_data.get("audio_url", get_audio_path(self.word))
        self.frequency = word_data.get("frequency", None)

    def __str__(self):
        return f'{self.word.upper()}\t\tLearning Stage: {self.learning_stage}\tFrequency: {self.frequency}\nTranslation:\n\t{self.get_translation("russian")}\nExamples: \n\t{self.get_examples()}TAGS:\n\t{self.tags}'

    def to_dict(self):
        return {
            "word": self.word,
            "translation": self.translation,
            "synonyms": self.synonyms,
            "definition": self.definition,
            "examples": self.examples,
            "part_of_speech": self.part_of_speech,
            "date_added": self.date_added,
            "last_reviewed": self.last_reviewed,
            "review_count": self._review_count,
            "learning_stage": self.learning_stage,
            "time_to_repeat": self.time_to_repeat,
            "notes": self.notes,
            "level": self.level,
            "tags": self.tags,
            "audio_url": self.audio_url,
            "frequency": self.frequency
        }

    def add_tags(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)
            logging.info(f'TAG: {tag} was added in {self.word}')

    def display_tags(self):
        return f'TAGS of {self.word}:' + '\n\t'.join(self.tags)

    def delete_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
            logging.info(f'TAG: {tag} was delete from word: {self.word.upper()}')

    def delete_level(self, level):
        if level in self.level:
            self.level.remove(level)
            logging.info(f'Level: {level} was deleted from word: {self.word.upper()}')

    def show_level(self):
        return ''.join(self.tags + ' ')

    def display_synonyms(self):
        return f'Synonyms :' + '\n'.join(self.synonyms) + '\n'

    def delete_synonym(self, synonym):
        if synonym not in self.synonyms:
            raise ValueError(f'Synonym: {synonym} not in {self.word} synonyms')

        self.synonyms.remove(synonym)
        logging.info(f'Synonym: {synonym.upper()} was deleted from word: {self.word.upper()}')

    def add_synonym(self, synonym):
        if synonym in self.synonyms:
            raise ValueError(f'Synonym {synonym} is already in synonyms')
        self.synonyms.append(synonym)
        logging.info(f'Synonym {synonym} was added to {self.word.upper} synonyms')

    def get_review_count(self):
        return self._review_count
    def update_last_reviewed(self):
        self.last_reviewed = utils.parse_to_str(utils.current_datetime())
        logging.info(f'Last reviewed of {self.word.upper()} was updated')

    def increase_review_count(self):
        if self._review_count <0:
            logging.error(f'REVIEW COUNTER IS LOWER THAN 0')
            raise ValueError(f'Review counter could not be a lower then 0!')
            logging.error(f'Word {self.word} have less then 0 reviews')
        self._review_count += 1
        logging.info(f'Review counter of word {self.word.upper()} is up')

    def __reset_review_count(self):
        self._review_count = 0
        logging.info(f'Review counter of word {self.word.upper()} was reseted')

    def get_definition(self):
        definitions = '\n'.join(self.definition)
        return definitions

    def display_definintion(self):
        print('\n'.join(self.definition))

    def pop_definiton(self):
        if len(self.definition) <=0:
            logging.error('INDEX ERROR: NO ITEMS')
            raise IndexError('No items in array. ')
        definition = self.definition[-1]
        self.definition = self.definition[:-1]
        logging.info(f'Definiton: {definition} was deleted')
        return definition

    def shift_definiton(self):
        if len(self.definition) <=0:
            logging.error(f'NO DEFINITION for {self.word}')
            raise IndexError('No items in array. ')
        definition = self.definition[0]
        self.definition = self.definition[1:]
        logging.info(f'Definiton: {definition} was deleted')
        return definition

    def set_time_to_repeat(self, minute):
        last_time = self.time_to_repeat
        self.time_to_repeat = utils.change_repeat_time(minute)
        logging.info(f'Time for repeate for word {self.word.upper()} was changed to {self.time_to_repeat} from {last_time}')
    def display_time_to_repeat(self):
        if self.time_to_repeat is None:
            raise ValueError(f'Time to repeate for word {self.word.upper()} was not set')
        print(utils.parse_time_to_str(self.time_to_repeat))

    def get_time_to_repeat(self):
        if self.time_to_repeat is None:
            raise ValueError(f'Time to repeate for word {self.word.upper()} was not set')
        return self.time_to_repeat

    def get_date_added(self):
        if self.date_added is None:
            raise ValueError(f'Added Date of word {self.word.upper()} was not set')
        return self.date_added

    def display_date_added(self):
        if self.date_added is None:
            raise ValueError(f'Added Date of word {self.word.upper()} was not set')
        print(utils.parse_time_to_str(self.date_added))

    def get_examples(self):
        if len(self.examples) == 0:
            logging.warning(f'Word {self.word} exclude examples!')
            return []
        return self.examples

    def display_examples(self):
        if len(self.examples) == 0:
            logging.warning(f'Word {self.word} exclude examples!')
        print(self.examples)

    def add_to_examples(self, example):
        if example in self.examples:
            logging.warning(f'Word {self.word} already contain examples: {example}!')
            raise ValueError(f'Word {self.word} already contain examples: {example}!')
        self.examples.append()
        return self.to_dict()

    def pop_example(self):
        if len(self.examples) <= 0:
            logging.error(f'You tried to pop example from empty array! Word: {self.word.upper()}')
            raise IndexError(f'Examples of word {self.word.upper()} are empty!')
        example = self.examples[-1]
        self.examples = self.examples[:-1]
        logging.info(f'From word {self.word.upper()} was pop example: {example}')
        return example

    def shift_example(self):
        if len(self.examples) <= 0:
            logging.error(f'You tried to shift example from empty array! Word: {self.word.upper()}')
            raise IndexError(f'Examples of word {self.word.upper()} are empty!')
        example = self.examples[0]
        self.examples = self.examples[1:]
        logging.info(f'From word {self.word.upper()} was pop example: {example}')
        return example

    def add_notes(self, note):
        if note in self.notes:
            logging.warning(f'You try to add duplicate of note')
            raise ValueError(f'Note: {note}\t is already in notes')
        self.notes.append(note)
        logging.info(f'In word: {self.word} was added a note [{note}]!')

    def pop_note(self):
        if len(self.notes) <= 0:
            logging.error(f'You tried to pop note from empty array! Word: {self.word.upper()}')
            raise IndexError(f'Notes of word {self.word.upper()} are empty!')
        note = self.notes[-1]
        self.notes = self.notes[:-1]
        logging.info(f'From word {self.word.upper()} was pop example: {note}')
        return note

    def shift_note(self):
        if len(self.notes) <= 0:
            logging.error(f'You tried to shift note from empty array! Word: {self.word.upper()}')
            raise IndexError(f'Notes of word {self.word.upper()} are empty!')
        note = self.notes[0]
        self.notes = self.notes[1:]
        logging.info(f'From word {self.word.upper()} was shift example: {note}')
        return note

    def increase_learning_stage(self):
        '''
        TODO: I need to write Observer that was informed about changes in learning stage
        :return: observer cahnge word vocabulary
        '''
        if self.learning_stage < 5:
            self.learning_stage += 1

    def down_learning_stage(self):
        if self.learning_stage == 0:
            raise IndexError('Learning stage could not be less than 0')
        self.learning_stage -= 1
        logging.info(f'Learning stage of word {self.word} was decrise by one. Now its: {self.learning_stage}')

    def display_part_of_speach(self):
        if len(self.part_of_speech) == 0:
            logging.info(f'Word: {self.word.upper()} does not contain part of speach')
            raise ValueError(f'No part of speech for word {self.word}')
        print(''.join(self.part_of_speech) + ' ')

    def get_part_of_speach(self):
        if len(self.part_of_speech) == 0:
            logging.info(f'Word: {self.word.upper()} does not contain part of speach')
            raise ValueError(f'No part of speech for word {self.word}')
        return self.part_of_speech

    def pop_part_of_speach(self):
       '''
       TODO:
            with part of speech should be removed exaamples related with that pos
       :return:
       '''
       pass

    def shift_part_of_speach(self):
        pass

    def add_part_of_speach(self):
        pass

    def display_translation(self):
        translation = ''
        for lang in self.translation.keys():
            translation += lang + '\n'
            for word in self.translation[lang]:
                translation += f'\t{word}\n'

        print(translation)

    '''
    TODO:
        refactor this functions 
        I dont like how they looks
    '''
    def remove_translation(self, lang):
        self.translation[lang].remove(self.word)

    def get_translation(self, lang):
        return self.translation[lang]

    def change_time_to_repeat(self,minutes):
        if self.time_to_repeat is None:
            logging.error(f'Time of word {self.word.upper()} was not initialized')
            raise ValueError(f'Time was not defined')
        print(f'TYPE OF DATE TO REPEAT  {type(self.time_to_repeat)}')
        return self.time_to_repeat + timedelta(minutes=minutes)
