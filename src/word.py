import json

import utils
from src.sound_manager import get_audio_path
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
        self.review_count = word_data["review_count"]
        self.learning_stage = word_data["learning_stage"]
        self.time_to_repeat = word_data["time_to_repeat"]
        self.notes = word_data.get("notes", [])
        self.level = word_data.get("level", None)
        self.tags = word_data.get("tags", [])
        self.audio_url = word_data.get("audio_url", get_audio_path(self.word))

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
            "review_count": self.review_count,
            "learning_stage": self.learning_stage,
            "time_to_repeat": self.time_to_repeat,
            "notes": self.notes,
            "level": self.level,
            "tags": self.tags,
            "audio_url": self.audio_url,
        }

    def add_tags(self,tag):
        if tag not in self.tags: self.tags.append(tag)
    def show_tags(self):
        return 'TAGS :' + '\n'.join(self.tags)


    def delete_tag(self,tag):
        if tag in self.tags: self.tags.remove(tag)

    def delete_level(self,level):
        if level in self.level: self.level.remove(level)

    def show_level(self):
        return ''.join(self.tags + ' ')

    def show_synonyms(self):
        return f'Synonyms :'+'\n'.join(self.synonyms)+'\n'

    def delete_synonym(self,synonym):
        if synonym in self.synonyms: self.synonyms.remove(synonym)

    def add_synonym(self,synonym):
        if synonym not in self.synonyms: self.synonyms.append(synonym)

    def update_last_reviewed(self):
        self.last_reviewed = utils.parse_to_str(utils.current_datetime())

    def increase_review_count(self):
        self.review_count +=1

    def __reset_review_count(self):
        self.review_count = 0

    def get_definition(self):
        definitions = '\n'.join(self.definition)
        return definitions

    def show_definintion(self):
        print('\n'.join(self.definition))
    def pop_definiton(self):
        if len(self.definition) >0:
            definition = self.definition[-1]
            self.definition=self.definition[:-1]
            print(f'Definiton: {definition} was deleted')
            return definition

    def shift_definiton(self):
        if len(self.definition) >0:
            definition = self.definition[0]
            self.definition=self.definition[1:]
            print(f'Definiton: {definition} was deleted')
            return definition
    def set_time_to_repeat(self,minute):
        self.time_to_repeat = utils.change_repeat_time(minute)
    def show_time_to_repeat(self):
        print(utils.parse_time_to_str(self.time_to_repeat))

    def get_time_to_repeat(self):
        return self.time_to_repeat

    def get_date_added(self):
        return self.date_added


    def show_date_added(self):
        print(utils.parse_time_to_str(self.date_added))

    def get_examples(self):
        return self.examples

    def show_examples(self):
        print(self.examples)
    def add_to_examples(self,example):
        self.examples.append()
        return self.to_dict()

    def pop_example(self):
        if len(self.examples) >0:
            example = self.examples[-1]
            self.examples = self.examples[:-1]
            return example

    def shift_example(self):
        if len(self.examples) >0:
            example = self.examples[0]
            self.examples = self.examples[1:]
            return example

    def add_notes(self,note):
        self.notes.append(note)
        print(f'In word: {self.word} was added a note!')
    def pop_note(self):
        if len(self.notes)<0:
            note = self.notes[-1]
            self.notes = self.notes[:-1]
            print(f'Note: {note} was deleted!')
    def shift_note(self):
        if len(self.notes)<0:
            note = self.notes[0]
            self.notes = self.notes[1:]
            print(f'Note: {note} was deleted!')

    def increase_learning_stage(self):
        if self.learning_stage < 5:
            self.learning_stage+=1

    def down_learning_stage(self):
        if self.learning_stage > 0:
            self.learning_stage-=1

    def show_part_of_speach(self):
        print(''.join(self.part_of_speech)+' ')
    def get_part_of_speach(self):
        return self.part_of_speech

    def pop_part_of_speach(self):
        pass

    def shift_part_of_speach(self):
        pass

    def add_part_of_speach(self):
        pass

    def show_translation(self):
        translation = ''
        for lang in self.translation.keys():
            translation += lang+'\n'
            for word in self.translation[lang]:
                translation += f'\t{word}\n'

        print(translation)

    def remove_translation(self,lang):
        self.translation[lang].remove(self.word)

    def get_translation(self,lang):
        return self.translation[lang]
