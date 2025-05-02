# Main entry point for the program
import json
import os.path
from pathlib import Path

from wolern.src.fetchers import cefr_from_csv_to_json
from wolern.src.text_scanner import load_text
from wolern.src.unchecked import get_sorted_unchecked, sort_unchecked_by_frequency, delete_from_unchecked
from wolern.src.utils import STANDART_VOCABULARY_PATH, STANDART_SORTED_UNCHECKED_PATH
from wolern.src.vocabulary import get_word_input, add_word_to_vocabulary, get_vocabulary, \
    show_all_vocabularies, get_list_of_new_words, show_vocabulary, update_learning_stage

input_message = (
    "\nSelect learning stage:\n"
    "  0: New word – not yet reviewed\n"
    "  1: Recognized – seen once or twice\n"
    "  2: Familiar – answered correctly once\n"
    "  3: Learned – answered correctly multiple times\n"
    "  4: Mastered – reviewed over time, rarely forgotten\n"
    "  5: Archived – fully known, rarely shown unless reset\n"
    "  q: To Exit.\n"
    "Enter your choice (0–5): "
)

def main():
    if os.path.exists('data/cache/cefr_cache.json'):
        cefr_from_csv_to_json()

    while True:
        print("\n=== Wolern Vocabulary Assistant ===")
        print("1. Add a new word manually")
        print("2. Scan a text file for unknown words")
        print("3. Show vocabulary list")
        print("4. Take a quiz")
        print("5. Review   words")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            # call add_word_to_vocabulary()
            add_word_to_vocabulary(get_word_input(),get_vocabulary(STANDART_VOCABULARY_PATH),1)
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
                show_vocabulary(get_vocabulary())
            else:
                show_vocabulary(get_vocabulary(vocabulary))
        elif choice == "4":
            # call quiz module
            pass
        elif choice == "5":
            vocabulary = get_vocabulary(STANDART_VOCABULARY_PATH)
            sort_unchecked_by_frequency(vocabulary)
            words = get_sorted_unchecked()

            while words:
                try:
                    word, freq = words.pop()  # use pop(0) to preserve sorting (FIFO)

                    print(f"\nReview word: {word} (frequency: {freq})")
                    stage = input(input_message)

                    if stage == 'q':
                        # Save progress back to sorted file
                        with open(STANDART_SORTED_UNCHECKED_PATH, "w", encoding="utf-8") as f:
                            json.dump(words, f, ensure_ascii=False, indent=2)
                        print("✅ Progress saved. Exiting review.")
                        break

                    if stage.isdigit() and 0 <= int(stage) <= 5:
                        if word in vocabulary:
                            update_learning_stage(word, int(stage), vocabulary, STANDART_VOCABULARY_PATH)
                        else:
                            add_word_to_vocabulary(word, STANDART_VOCABULARY_PATH, int(stage))
                    else:
                        print("⚠️ Invalid input. Enter a number from 0–5 or 'q' to quit.")
                except Exception as e:
                    print(f"❌ Error during review: {e}")
                    break
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()