import rich
from rich.progress import Progress, SpinnerColumn, TextColumn

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
import fetchers
from src.vocabulary import Vocabulary_Manager,Vocabulary
import pprint


def main():
    while True:
        command = input(f'Write a command:\nc'
                        f'lean: if you want to clean vocabulary\n'
                        f'show : show vocabulary\n'
                        f'word: get word\n'
                        f'size: print size of vocabulary\n'
                        f'exit: to close the app\n')

        if command == 'clean':
            vocabulary_name = input('What vocabulary\n')
            manager = Vocabulary_Manager()
            manager.clean_vocabulary(vocabulary_name)
        elif command == 'show':
            vocabulary = Vocabulary('known')
            pprint.pprint(vocabulary.vocabulary)
        elif command == 'word':
            while True:
                word_command = input(f'\nWrite a command :\n'
                                     f'words_in: show list of words'
                                     f'definit: if you whant to get definition of the word\n'
                                     f'add : add word to vocabulary\n'
                                     f'delete: to delete word from vocabulary\n'
                                     f'example: to show examples\n'
                                     f'exit: to change to previously\n')
                if word_command == 'definit':
                    word = input('input word\n')
                    voc = Vocabulary('known')
                    if voc.is_word_in_vocabulary(word): print(voc.get_word_from_vocabulary(word).get_definition())
                elif word_command == 'delete':
                            word = input('input word:\n')
                            if voc.is_word_in_vocabulary(word):Vocabulary('known').delete_word_from_vocabulary(word)
                elif word_command == 'add':
                    word = input('input word:\n')

                    if not Vocabulary('known').is_word_in_vocabulary(word):Vocabulary('known').add_word_to_vocabulary(word)
                elif word_command == 'example':
                    word = input('input word\n')
                    if Vocabulary('known').is_word_in_vocabulary(word):
                        word = Vocabulary('known').get_word_from_vocabulary(word)
                        word.show_examples()
                elif word_command == 'words_in':
                    voc = Vocabulary('known').get_list_of_words()
                    print(voc)
                elif word_command == 'exit':
                    break
        elif command == 'size':
            pprint.pprint(Vocabulary('known').get_size())
        elif command == 'exit':
            pprint.pprint(f'See later!')
            break
        



# def main():
#     if os.path.exists('data/cache/cefr_cache.json'):
#         cefr_from_csv_to_json()
#
#     while True:
#         print("\n=== Wolern Vocabulary Assistant ===")
#         print("1. Add a new word manually")
#         print("2. Scan a text file for unknown words")
#         print("3. Show vocabulary list")
#         print("4. Take a quiz")
#         print("5. Review   words")
#         print("6. Exit")
#
#         choice = input("Choose an option: ")
#
#         if choice == "1":
#             # call add_word_to_vocabulary()
#             add_word_to_vocabulary(get_word_input(), Path(__file__).resolve().parent / 'data' / 'vocabularies' / 'vocabulary.json', 1)
#         elif choice == "2":
#             # call text scanning logic
#             limit = int(input("How many new words you want to add\nPrint zero to no limit\Write a number : "))
#             path_to = Path(input("Write a path to file: "))
#             if limit == 0:
#                 load_text(path_to)
#             else:
#                 load_text(path_to, limit)
#         elif choice == "3":
#             # display saved words
#             vocabulary = input(
#                 f'write a name of vocabulary to show there contant :{show_all_vocabularies()}\nPress Enter to show defualt vocabulary')
#             if len(vocabulary) == 0:
#                 show_vocabulary(get_vocabulary())
#             else:
#                 show_vocabulary(get_vocabulary(Path(__file__).resolve().parent / 'data' / 'vocabularies'/ vocabulary))
#         elif choice == "4":
#             # call quiz module
#             pass
#         elif choice == "5":
#             vocabulary = get_vocabulary(STANDART_VOCABULARY_PATH)
#             sort_unchecked_by_frequency(vocabulary)
#             words = get_sorted_unchecked()
#
#             while words:
#                 try:
#                     word, freq = words.pop()  # use pop(0) to preserve sorting (FIFO)
#
#                     print(f"\nReview word: {word} (frequency: {freq})")
#                     stage = input(input_message)
#
#                     if stage == 'q':
#                         # Save progress back to sorted file
#                         with open(STANDART_SORTED_UNCHECKED_PATH, "w", encoding="utf-8") as f:
#                             json.dump(words, f, ensure_ascii=False, indent=2)
#                         print("✅ Progress saved. Exiting review.")
#                         break
#
#                     if stage.isdigit() and 0 <= int(stage) <= 5:
#                         if word in vocabulary:
#                             update_learning_stage(word, int(stage), vocabulary, STANDART_VOCABULARY_PATH)
#                         else:
#                             add_word_to_vocabulary(word, STANDART_VOCABULARY_PATH, int(stage))
#                     else:
#                         print("⚠️ Invalid input. Enter a number from 0–5 or 'q' to quit.")
#                 except Exception as e:
#                     print(f"❌ Error during review: {e}")
#                     break
#         elif choice == "6":
#             print("Goodbye!")
#             break
#         else:
#             print("Invalid choice. Please try again.")
#

if __name__ == "__main__":
    main()
