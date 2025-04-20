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

## 🛠 Installation

1. Clone the repo.
2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## 🛠 Usage

> Work in progress — command-line and GUI examples will be added.

## 📌 Roadmap

- [x] Define project goal — create a tool to help learn English words from real texts.
- [x] Design JSON vocabulary structure — store words, translations, synonyms, and meanings.

### 🧠 Implement Core Logic
- [x] Create word entry matching final schema.
- [ ] Load existing vocabulary from JSON file.
- [ ] Save updated vocabulary to JSON.
- [ ] Scan and clean text files.
- [ ] Compare words with saved vocabulary.
- [ ] Fetch missing data using external libraries (translation, synonyms, meanings).

### 💻 CLI Menu & Main Loop
- [x] Add main process loop structure (text menu).
- [ ] Implement “Add new word” option.
- [ ] Implement “Scan text for unknown words” option.
- [ ] Implement “Show vocabulary list” option.
- [ ] Implement “Quiz mode” option.
- [ ] Allow clean exit (basic and stable).

### 🖼 GUI & Testing (Next Stages)
- [ ] Develop basic Tkinter GUI.
- [ ] Write unit tests for core logic.
- [ ] Plan and prepare migration to web version (Flask or Django).
## 🧑‍💻 Contributing

Right now this is a solo learning project, but contributions are welcome for feedback, ideas, or suggestions.

---

