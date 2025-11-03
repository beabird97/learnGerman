# Learn German - Family Language Learning App

A simple, interactive web application for learning German vocabulary and verb conjugations. Designed for family use on a local network.

## Features

- **User Management**: Three users (sam, sheryl, chris) with individual progress tracking
- **Vocabulary Learning**: Study 231 German nouns with proper articles (der/die/das)
- **Verb Conjugations**: Practice 78 German verbs in present tense with full conjugation tables
- **Interactive Practice**: Click-through learning with immediate feedback
- **Mock Tests**: Practice tests (10 questions) with instant feedback
  - Choose direction: German → English or English → German
- **Real Tests**: Graded tests (20 questions, English → German only) with final scoring (A-F)
- **Progress Tracking**: Monitor time spent, words learned, test results with visual progress bars and trending graphs
- **Activity Monitoring**: Automatic time tracking with 5-minute inactivity timeout
- **Smart Learning**: Prioritizes words/verbs that are unseen or frequently incorrect

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```bash
   python init_db.py
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

### Running on Raspberry Pi

To run on a Raspberry Pi accessible on your local network:

1. Follow the installation steps above

2. The app is already configured to run on `0.0.0.0:8000`

3. Find your Raspberry Pi's IP address:
   ```bash
   hostname -I
   ```

4. Access from any device on your network:
   ```
   http://[raspberry-pi-ip]:8000
   ```

**Note**: Port 8000 is used instead of 5000 to avoid conflicts with macOS AirPlay Receiver.

## User Accounts

- **Username**: sam | **Password**: sam
- **Username**: sheryl | **Password**: sheryl
- **Username**: chris | **Password**: chris

## Project Structure

```
learnGerman/
├── app.py              # Main Flask application
├── models.py           # Database models
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── progress.html
│   ├── learn_vocabulary.html
│   ├── learn_verbs.html
│   ├── mock_test.html
│   ├── real_test.html
│   └── test_complete.html
├── venv/              # Python virtual environment
└── instance/          # Flask instance folder
    └── learnGerman.db # SQLite database (created after init)
```

## Technology Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **Database**: SQLite with Flask-SQLAlchemy 3.1.1
- **Frontend**: Bootstrap 5 for UI, JetBrains Mono font
- **Charts**: Chart.js for progress visualization

## Usage

### Learning Vocabulary
1. Click "Learn Vocabulary" on the dashboard
2. View German words with articles (der/die/das)
3. Click to reveal English translation
4. Mark correct/incorrect - system prioritizes words you need to practice

### Learning Verbs
1. Click "Learn Verbs" on the dashboard
2. Study the conjugation table
3. Practice in the "Now You Do It" section
4. Submit to check your answers

### Taking Tests

**Mock Tests** (Practice mode)
- 10 random questions
- Choose German → English or English → German
- Instant feedback per question
- Results saved to progress

**Real Tests** (Graded mode)
- 20 questions, English → German only
- No feedback until completion
- Graded A-F: A(90-100%), B(80-89%), C(70-79%), D(60-69%), F(<60%)

### Answer Validation

The system is flexible:
- **German → English**: Accepts "bank" or "the bank"
- **English → German**: Accepts "Bank" or "die Bank"
- Case insensitive

## Database Schema

- **user**: User accounts (3 users)
- **word**: 231 German nouns with articles
- **verb**: 78 German verbs with conjugations
- **user_progress**: Overall learning statistics per user
- **word_progress**: Individual word tracking (seen, correct, incorrect)
- **verb_progress**: Individual verb tracking
- **test_result**: Test scores and history
- **test_answer**: Individual question answers
- **activity_log**: Session time tracking

## Maintenance Scripts

- `init_db.py` - Initialize database with users and vocabulary
- `add_more_vocabulary.py` - Add additional words/verbs (checks for duplicates)
- `cleanup_words.py` - Remove non-nouns or words without articles
- `delete_words_after_105.py` - Example: Delete specific words safely

## Troubleshooting

**Database Locked Error**
- Ensure database is not open in another program
- Remove stale `.db-journal` files if needed

**Port 8000 Already in Use**
- Change port in `app.py` (line ~500)
- Or kill existing process: `pkill -f "python app.py"`

## Security Note

This app is designed for **local network use only**:
- Simple authentication (password = username)
- No HTTPS
- Debug mode enabled
- Do not expose to public internet

## Additional Documentation

- `CODE_GUIDE.md` - Detailed code architecture and how it works
- `TODO.md` - Future enhancements and task list
- `REQUIREMENTS.md` - Complete feature requirements
