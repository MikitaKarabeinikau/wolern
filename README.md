# Wolern  ![Python](https://img.shields.io/badge/Python-3.12-blue) ![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

 

<table>
<tr>
<td width="40%">
  <img src="images/wide_version.png" alt="Wolern Banner" width=100% height="300"/>
</td>
<td>
  <p><strong>Wolern is a Python-based personal project designed to help me (and others) learn English vocabulary effectively using technology.</strong></p>
  <p>The project aims to combine basic programming, Natural Language Processing (NLP) techniques, and interactive exercises.</p>
  <p>Personal project combining Python, NLP, and smart exercises.</p>
</td>
</tr>
</table>
<p align="left">
  
</p>

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
# 📍 Wolern Project Roadmap (Updated)

## ✅ Phase 1: Core CLI App
- [x] Define project goal.
- [x] Design vocabulary JSON structure.
- [x] Set up virtual environment and base folders.
- [x] Implement manual word adding.
- [x] Load and display existing vocabulary from JSON.
- [x] Fetch synonyms, definitions, POS, CEFR level.
- [x] Save audio pronunciation paths.
- [x] Build basic text scanner for `.txt` files.

---

## ✅ Phase 2: CLI Main Features
- [x] CLI menu with 5 options: add, scan, show vocab, quiz, exit.
- [x] Show vocabulary list (pretty format).
- [ ] Quiz mode (multiple choice planned).
- [ ] Save and load vocabulary reliably.
- [ ] Clean and graceful exit.

---

## 🧠 Phase 3: Unchecked Words Processing
> **Goal: Manage unknown scanned words smartly.**

### Unchecked Words Management
- [x] Save scanned unknown words into `unchecked_words.json`.
- [ ] CLI function to review unchecked words manually:
  - Accept → fetch full data → add to vocabulary.
  - Reject → move to ignored words.
  - Skip → leave for later.
- [ ] Save rejected words (`ignored_words.json`) with reason tags.
- [ ] Allow CLI to set dynamic `load_limit` for scanning.

### Popularity/Frequency Tracking
- [ ] Add `frequency_rank` and `popularity` fields to word structure.
- [ ] Fetch frequency data along with other word info.
- [ ] Store popularity info for smarter processing.

### Smart Unloading System
- [ ] Create popularity-sorted array (`unchecked_priority_list`).
- [ ] During CLI idle time (between user actions), process a few unchecked words:
  - Prioritize easy/common words first.
  - Fetch and complete their info automatically.
- [ ] Allow settings like "Process 5 words per idle pause."

---

## 🔵 Phase 4: GUI Prototype (Tkinter)
- [ ] Build simple GUI for adding and managing words.
- [ ] GUI to launch quizzes.
- [ ] Show stats and progress in GUI.
- [ ] Handle vocabulary file operations from GUI.

---

## 🔵 Phase 5: Web App Version (Flask or FastAPI)
- [ ] Set up backend API for vocabulary management.
- [ ] Create frontend (HTML/Bootstrap/TailwindCSS).
- [ ] Add optional login/authentication system.
- [ ] Deploy Web App to free hosting (Render, Vercel, etc.).

---

## ✍️ Phase 6: Documentation & Polish
- [ ] Expand README with usage examples, screenshots.
- [ ] Add LICENSE file (MIT or similar).
- [ ] Write CONTRIBUTING.md (optional).
- [ ] Add small promotional materials (like GIFs, demo videos).

---

## 🧪 Phase 7: Testing & Stability
> **Goal: Ensure reliability and maintainability.**

- [ ] Unit tests for vocabulary loading/saving.
- [ ] Tests for text scanning and word processing.
- [ ] Tests for CLI interaction flow.
- [ ] Error handling tests (missing files, wrong input).
- [ ] Performance tests (large vocabulary, big text scans).

---

# 🎯 MVP Target
✅ CLI where you can:
- Add new words.
- Scan `.txt` files for unknown words.
- Manage unchecked and ignored words.
- Save full vocabulary enriched with POS, CEFR, synonyms, popularity.
- Take quizzes on learned words.

---

# 🛣️ Project Phases Summary
| Phase | Name |
|:------|:-----|
| Phase 1 | Core CLI App |
| Phase 2 | CLI Main Features |
| Phase 3 | Unchecked Words Processing (priority-based) |
| Phase 4 | GUI Prototype (Tkinter) |
| Phase 5 | Web App Version (Flask/FastAPI) |
| Phase 6 | Documentation & Polish |
| Phase 7 | Testing & Stability |

---
---
## 🧑‍💻 Contributing

Right now this is a solo learning project, but contributions are welcome for feedback, ideas, or suggestions.

---

### Data sources 
** CEFR‑J Vocabulary & Grammar Profile
* ** — © Tono Laboratory, TUFS.  Used under the terms: “CEFR‑J vocabulary and grammar profile datasets can be used for research and commercial purposes with no charge, provided that you cite the dataset properly.” 
* **Octanove Vocabulary Profile (C1/C2)
* ** — Licensed under CC BY‑SA 4.0.
