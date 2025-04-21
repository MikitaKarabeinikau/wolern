from wolern.wolern.vocabulary  import get_synonyms
from wolern.wolern.vocabulary import get_parts_of_speech


def test_get_synonyms():
    word = "focus"
    synonyms = get_synonyms(word)
    print(f"Synonyms for '{word}':\n{synonyms}")

def test_get_part_of_speech():
    word = "focus"
    part_of_speech  = get_parts_of_speech(word)
    print(f'Word: {word} => Part of speech {part_of_speech}')

if __name__ == "__main__":
    test_get_part_of_speech()