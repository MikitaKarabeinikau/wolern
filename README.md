# Wolern

Wolern is a Python-based personal project designed to help me (and others) learn English vocabulary effectively using technology. The project aims to combine basic programming, Natural Language Processing (NLP) techniques, and interactive exercises.

## 🎯 Project Goals

- Improve and expand English vocabulary.
- Use Python to develop learning tools.
- Experiment with NLP libraries like NLTK, spaCy, and Hugging Face.
- Practice project management and software development skills.

## ⚙️ Features (Planned)

- Word collection and saving.
- Automatic definition and example sentence fetcher.
- Flashcard-style review system.
- Simple command-line or web interface.
- Quizzes for active recall.
- Progress tracking.

## 📚 Tech Stack

- Python 3.x
- NLP Libraries:
  - spaCy
  - NLTK
  - Hugging Face Transformers (for examples)
- SQLite or JSON for storing words.
- (Future) Web Framework: Flask or FastAPI.

## 💡 Why this project?

As a non-native English speaker and programming learner, I created Wolern to:
- Combine language learning with coding practice.
- Apply software engineering principles.
- Have fun with real data and NLP!

## 🚀 Installation

> Work in progress — when the first version is ready, instructions will appear here.

## 🛠 Usage

> Work in progress — command-line and GUI examples will be added.

## 📌 Roadmap

- [ ] Create basic word list management.
- [ ] Integrate word definitions (dictionary API or local file).
- [ ] Add example sentence fetcher.
- [ ] Develop quiz module.
- [ ] Design simple interface.
- [ ] Add progress tracking.

---

## 🧑‍💻 Contributing

Right now this is a solo learning project, but contributions are welcome for feedback, ideas, or suggestions.

---

## Explanation of the Structure
main.py
Purpose: 
- This is where your program starts running. It will be the central place to call functions from other modules, essentially controlling the program's flow.

Content:

- Import all the necessary functions (from other .py files).

- Display a simple text menu with options: Add a word, List words, Take a quiz, Scan a text, etc.

- Handle user input and direct them to the appropriate function from vocabulary.py, quiz.py, etc.

Why:

>Keeping the entry point separate (in main.py) makes the program modular and easier to scale. When you want to update or expand the logic, it's isolated in main.py.

vocabulary.py
Purpose: 
- This file is for everything related to managing your vocabulary.

Content:

- Functions to add words to the vocabulary.

- Functions to list words from your vocabulary.

- Remove or update words.

- This file will interact with the word_list.json file to read and write data.

Why:

> This keeps the logic for managing words in one place.

It makes it easier to change how words are stored or manipulated in the future without interfering with other parts of the code.

text_scanner.py
Purpose: This will handle the functionality of loading and processing text files.

Content:

Functions to open text files.

Split text into individual words.

Analyze words (check if they exist in the vocabulary, or if they need to be added).

Why:

This functionality should be separate from vocabulary management because it’s a different task — you're reading and processing external files, not just managing your internal word list.

dictionary_api.py
Purpose: This file is for handling interactions with external APIs (such as dictionaries and translation services).

Content:

Functions to fetch word meanings, translations, examples, and any other relevant information using libraries like NLTK, PyDictionary, or external APIs.

Why:

Keeping API calls in one place makes it easier to manage and switch between APIs if needed (e.g., if you decide to change the dictionary API, you only have to change it here).

quiz.py
Purpose: This file is dedicated to the quiz or test functionality.

Content:

Functions to generate quizzes, ask questions, and check answers.

This could be as simple as asking the user to translate a word or choose the correct meaning from a list.

Why:

Separating quiz-related logic keeps things focused and organized. You can easily modify the quiz without affecting other parts of the program.

progress_tracker.py
Purpose: This file will be responsible for keeping track of which words you’ve reviewed and how often.

Content:

Functions to track review dates for words.

Functions to calculate when a word should be reviewed next (for spaced repetition).

Why:

Keeping the progress tracker separate lets you easily extend or modify how you track progress without touching other parts of your program.

word_list.json
Purpose: This is your data storage file.

Content:

A list of words in JSON format. Each word entry will have:

word

meaning

translation

example

review count

added date

Why:

Using a JSON file to store data allows you to easily load and save data without using a full database. It’s lightweight, and it’s easy to work with in Python.