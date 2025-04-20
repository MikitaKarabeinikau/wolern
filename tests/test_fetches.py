from wolern.wolern.vocabulary  import get_synonyms


def test_get_synonyms():
    word = "focus"
    synonyms = get_synonyms(word)
    print(f"Synonyms for '{word}':\n{synonyms}")

if __name__ == "__main__":
    test_get_synonyms()