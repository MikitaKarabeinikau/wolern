# Wolern  
![Python](https://img.shields.io/badge/Python-3.12-blue) 
![FastAPI](https://img.shields.io/badge/FastAPI-0.116.1-green)
![React](https://img.shields.io/badge/React-Latest-61dafb)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

<div align="center">
  <img src="backend/data/images/wide_version.png" alt="Wolern Banner" width="600"/>
</div>

## 📖 Overview

**Wolern** is a modern, intelligent web application designed for vocabulary learning and language progress tracking. It provides a comprehensive platform for learners to expand their vocabulary through interactive exercises, spaced repetition, and personalized learning paths.

The application combines a robust FastAPI backend with a responsive React frontend to deliver a seamless learning experience with features like word management, quiz generation, translation services, and progress tracking.

## ✨ Key Features

### 🎯 Core Functionality
- **Vocabulary Management**: Create, organize, and manage multiple vocabularies
- **Intelligent Word Addition**: Automated word validation with CEFR level detection
- **Smart Exercises**: Multiple exercise types including:
  - Input answer exercises
  - Multiple choice questions
  - Interactive quizzes with spaced repetition
- **Translation Services**: Integrated translation and definition fetching
- **Audio Pronunciation**: Text-to-speech support for word pronunciation
- **Progress Tracking**: Comprehensive statistics and learning analytics

### 🔍 Advanced Features
- **CEFR Level Classification**: Automatic word difficulty assessment using CEFR-J standards
- **Frequency Analysis**: Word usage frequency data from SUBTLEX-US corpus
- **Synonym Management**: Build connections between related words
- **Warning System**: Validate words before adding them to vocabulary
- **User Authentication**: Secure authentication via Clerk
- **API Quotas**: Usage tracking and quota management

## 🛠 Technology Stack

### Backend
- **Framework**: FastAPI 0.116.1
- **Database**: SQLAlchemy with PostgreSQL
- **Authentication**: Clerk webhooks and JWT
- **NLP**: NLTK for text processing
- **Translation**: DeepL API, Google Translate
- **Audio**: gTTS (Google Text-to-Speech)
- **Testing**: pytest

### Frontend
- **Framework**: React with Vite
- **Routing**: React Router
- **Authentication**: Clerk React
- **Styling**: CSS with modern design patterns

### Development Tools
- **Database Migration**: Alembic
- **Environment Management**: python-dotenv
- **Code Quality**: ESLint

## 📁 Project Structure

```
wolern/
├── backend/                    # Backend application
│   ├── src/
│   │   ├── core/              # Core business logic
│   │   │   ├── word.py        # Word management
│   │   │   ├── vocabulary.py  # Vocabulary operations
│   │   │   ├── quiz.py        # Quiz generation
│   │   │   ├── fetchers.py    # External API integrations
│   │   │   └── tests/         # Unit tests
│   │   ├── routes/            # API endpoints
│   │   │   ├── words.py       # Word CRUD operations
│   │   │   ├── quiz.py        # Quiz endpoints
│   │   │   ├── exercise.py    # Exercise endpoints
│   │   │   ├── translations.py
│   │   │   └── user.py
│   │   └── database/          # Database models and schemas
│   ├── data/                  # Data files and sources
│   │   ├── images/            # Application images
│   │   └── source/            # CEFR and frequency data
│   ├── app.py                 # FastAPI application
│   └── server.py              # Server entry point
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── features/          # Feature-specific components
│   │   │   ├── auth/          # Authentication
│   │   │   ├── vocabularies/  # Vocabulary management
│   │   │   ├── exerciese/     # Exercise system
│   │   │   ├── quiz/          # Quiz interface
│   │   │   └── statistics/    # Progress tracking
│   │   ├── layout/            # Layout components
│   │   └── api/               # API client
│   └── index.html             # Entry HTML
├── alembic/                   # Database migrations
├── main.py                    # CLI interface
├── requirements.txt           # Python dependencies
└── setup.py                   # Package setup

```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher (3.12 recommended)
- Node.js and npm (for frontend)
- PostgreSQL database
- Clerk account for authentication

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/MikitaKarabeinikau/wolern.git
cd wolern
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://user:password@localhost/wolern
CLERK_SECRET_KEY=your_clerk_secret_key
OPENAI_API_KEY=your_openai_key  # Optional
DEEPL_API_KEY=your_deepl_key    # Optional
```

5. **Initialize the database**
```bash
alembic upgrade head
```

6. **Run the backend server**
```bash
python backend/server.py
# or use uvicorn directly:
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
Create a `.env` file in the `frontend` directory:
```env
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
VITE_API_URL=http://localhost:8000
```

4. **Start the development server**
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📚 Usage

### Web Interface

1. **Sign Up/Login**: Access the application and authenticate via Clerk
2. **Create Vocabulary**: Start by creating a new vocabulary collection
3. **Add Words**: Add words manually or import from text
4. **Practice**: Use exercises and quizzes to learn
5. **Track Progress**: Monitor your learning statistics

### CLI Interface

For development and testing, a CLI is available:

```bash
python main.py
```

Available commands:
- `def`: Get word definition
- `word`: Look up word information
- `quiz`: Start quiz mode
- `vocabulary`: Manage vocabularies
- `test`: Generate test data

## 🔌 API Documentation

Once the backend is running, interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `GET /`: API health check
- `POST /words/add`: Add a new word
- `GET /words/{word_id}`: Get word details
- `POST /exercise/generate`: Generate exercises
- `GET /quiz/`: Get quiz questions
- `POST /webhooks/clerk`: Clerk authentication webhook

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest backend/src/core/tests/test_vocabulary.py

# Run with coverage
pytest --cov=backend/src
```

## 🗃 Data Sources

This project uses the following linguistic datasets:

### CEFR-J Vocabulary & Grammar Profile
- **Source**: © Tono Laboratory, Tokyo University of Foreign Studies
- **License**: Free for research and commercial use with proper citation
- **Usage**: Word difficulty classification (A1-C2 levels)

### Octanove Vocabulary Profile (C1/C2)
- **License**: CC BY-SA 4.0
- **Usage**: Advanced vocabulary classification

### SUBTLEX-US
- **Source**: Brysbaert & New (2009)
- **License**: Free for research and educational purposes
- **Usage**: Word frequency data from American English subtitle corpora

For detailed licensing information, see [DATA_LICENSES.md](DATA_LICENSES.md)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript/React code
- Write tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Mikita Karabeinikau**

- GitHub: [@MikitaKarabeinikau](https://github.com/MikitaKarabeinikau)
- Project Repository: [wolern](https://github.com/MikitaKarabeinikau/wolern)

## 🙏 Acknowledgments

- CEFR-J Project at Tokyo University of Foreign Studies
- Octanove Labs for vocabulary profiles
- Brysbaert & New for SUBTLEX-US corpus
- The open-source community

## 📮 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Contact the maintainer through GitHub

---

**Note**: This project is currently in active development. Features and documentation may change as the project evolves.
