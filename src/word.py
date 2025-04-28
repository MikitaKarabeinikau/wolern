import json

from wolern.src.sound_manager import get_audio_path
from wolern.src.vocabulary import word_in_vocabulary


class Word:
    def __init__(self,word_data:dict):
            self.word = word_data["word"]
            self.translation = word_data["translation"]
            self.synonyms = word_data.get("synonyms",[])
            self.definition = word_data.get("definition",[])
            self.examples = word_data.get("examples",[])
            self.part_of_speech = word_data["part_of_speech"]
            self.date_added = word_data["date_added"]
            self.last_reviewed = word_data["last_reviewed"]
            self.review_count = word_data["review_count"]
            self.learning_stage = word_data["learning_stage"]
            self.time_to_repeat = word_data["time_to_repeat"]
            self.notes = word_data.get("notes",[])
            self.level = word_data.get("level",None)
            self.tags = word_data.get("tags",[])
            self.audio_url = word_data.get("audio_url",get_audio_path(self.word))

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

    def save_word_in_vocabulary(self,vocabulary):
        if not word_in_vocabulary(self.word,vocabulary):
                vocabulary[self.word] = self.to_dict()
                with open(vocabulary,"w",encoding="utf-8") as f:
                        json.dump(vocabulary,f,ensure_ascii=False,indent=2)
