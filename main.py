# Main entry point for the program

from wolern.vocabulary import get_word_input, add_word_to_vocabulary

def main():
    while True:
        print("\n=== Wolern Vocabulary Assistant ===")
        print("1. Add a new word manually")
        print("2. Scan a text file for unknown words")
        print("3. Show vocabulary list")
        print("4. Take a quiz")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            # call add_word_to_vocabulary()
            add_word_to_vocabulary(get_word_input())
            pass
        elif choice == "2":
            # call text scanning logic
            pass
        elif choice == "3":
            # display saved words
            pass
        elif choice == "4":
            # call quiz module
            pass
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()