# Main entry point for the program
import os.path
from pathlib import Path

from wolern.src.fetchers import cefr_from_csv_to_json
from wolern.src.text_scanner import load_text
from wolern.src.vocabulary import get_word_input, add_word_to_vocabulary, show_vocabulary_list, get_vocabulary, \
    show_all_vocabularies


def main():
    if os.path.exists('data/cache/cefr_cache.json'):
        cefr_from_csv_to_json()

    while True:
        print("\n=== Wolern Vocabulary Assistant ===")
        print("1. Add a new word manually")
        print("2. Scan a text file for unknown words")
        print("3. Show vocabulary list")
        print("4. Take a quiz")
        print("5. Review new words")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            # call add_word_to_vocabulary()
            add_word_to_vocabulary(get_word_input())

        elif choice == "2":
            # call text scanning logic
            limit = int(input("How many new words you want to add\nPrint zero to no limit\Write a number : "))
            path_to = Path(input("Write a path to file: "))
            if limit == 0:
                load_text(path_to)
            else:
                load_text(path_to,limit)

        elif choice == "3":
            # display saved words
            vocabulary = input(f'write a name of vocabulary to show there contant :{show_all_vocabularies()}\nPress Enter to show defualt vocabulary')
            if len(vocabulary) == 0:
                show_vocabulary_list(get_vocabulary())
            else:
                show_vocabulary_list(get_vocabulary(vocabulary))
        elif choice == "4":
            # call quiz module
            pass
        elif choice == "5":
            while True:
                pass
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()