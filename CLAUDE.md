# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Flask-based web application for learning German vocabulary and verb conjugations. Designed for family use on a local network (Raspberry Pi). Features user-specific progress tracking, interactive learning modules, mock tests with instant feedback, and graded real tests.

## Common Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database (first time setup or reset)
python init_db.py

# Run development server
python app.py

# Access locally
# http://localhost:8000

# Access on local network (Raspberry Pi)
# http://[raspberry-pi-ip]:8000

# Note: Port 8000 is used to avoid conflicts with macOS AirPlay (port 5000)
```

### Database Operations
- Database file: `instance/learnGerman.db` (SQLite)
- To reset database: Delete `instance/learnGerman.db` and run `python init_db.py`
- Database is automatically created in the `instance/` folder on first `init_db.py` run
- The `instance/` folder is used by Flask for instance-specific files

## Architecture

### Application Structure

**app.py** - Main Flask application
- All route handlers and application logic
- Session-based authentication (no password hashing - local network only)
- Activity tracking middleware (`before_request`, `update_activity`)
- Routes organized by feature: auth, learning, testing, progress

**models.py** - SQLAlchemy database models
- `User`: Three hardcoded users (sam, sheryl, chris)
- `Word`: 100 German nouns with articles (der/die/das) and English translations
- `Verb`: 30 German verbs with present tense conjugations (ich, du, er/sie/es, wir, ihr, sie/Sie)
- `UserProgress`: Aggregate statistics per user
- `WordProgress`, `VerbProgress`: Per-item learning statistics
- `TestResult`: Test scores and metadata
- `TestAnswer`: Individual test question answers
- `ActivityLog`: Time tracking with start/end timestamps

**init_db.py** - Database initialization
- Creates tables and populates initial data
- Idempotent (checks if data exists before inserting)
- Run this after any model changes or to reset data

### Key Design Patterns

**Session Management**
- Flask session stores: `user_id`, `username`, `last_activity`, `activity_log_id`
- Test sessions store: `test_questions`, `test_type`, `is_mock`, `current_question`, `test_score`, `test_answers`
- Activity tracking: 5-minute inactivity timeout automatically ends activity logs

**Smart Content Selection**
- Learn vocabulary/verbs prioritize:
  1. Items never seen
  2. Items with more incorrect than correct answers
  3. Random selection from all items if no priority items

**Progress Tracking**
- `update_activity()` called before each request
- If inactive >5 minutes: ends previous ActivityLog, starts new one
- Duration calculated on activity end, added to user's total time
- All learning and test interactions update WordProgress/VerbProgress

**Test Flow**
- Mock tests: 10 questions, instant feedback per question
- Real tests: 20 questions, no feedback until completion, graded (A-F)
- Session stores question IDs, answers collected progressively
- On completion: save TestResult, TestAnswers, update progress tables

### Frontend Architecture

**Base Template** (`templates/base.html`)
- Bootstrap 5 for UI components
- JetBrains Mono font for modern look
- Gradient backgrounds and card-based layout
- Navbar with user info and logout (shown when authenticated)
- Consistent button styles with hover effects

**Interactive Features**
- Learn verbs: Toggle between display and practice modes with AJAX validation
- Mock tests: AJAX submission with instant feedback
- Real tests: Progressive submission, no answer review
- Progress page: Chart.js for mock test trends visualization

**Styling Conventions**
- Gradient buttons (primary, success, info, warning, danger)
- Card-based content containers with shadows
- Large, centered German words (3rem font)
- Color-coded feedback (green=correct, red=incorrect)
- Grade colors: A=green, B=blue, C=yellow, D=pink, F=red

## Database Schema Notes

### Important Relationships
- All progress tables (`UserProgress`, `WordProgress`, `VerbProgress`, `TestResult`, `ActivityLog`) have `user_id` foreign key
- `TestAnswer` links to `TestResult` and either `Word` or `Verb` (one will be null)
- `WordProgress`/`VerbProgress` track: times_seen, times_correct, times_incorrect, last_seen

### Adding Vocabulary/Verbs
Edit `init_db.py`:
- Words: Add tuples to `words` list as `(german, english, article)`
- Verbs: Add tuples to `verbs` list as `(infinitive, english, ich, du, er_sie_es, wir, ihr, sie_Sie)`
- Delete `learnGerman.db` and run `python init_db.py` to apply changes

## Common Modifications

### Adding a New User
1. Edit `init_db.py` users list: `User(username='name', password='pass')`
2. Reset database

### Changing Test Parameters
In `app.py`:
- Mock test count: Change `.limit(10)` in `mock_test()` route
- Real test count: Change `.limit(20)` in `real_test()` route
- Inactivity timeout: Change `300` seconds in `update_activity()`

### Modifying Smart Selection Logic
See `learn_vocabulary()` and `learn_verbs()` routes:
- Adjust priority criteria in the logic that builds `priority_words`/`priority_verbs`

### Adding New Learning Modes
1. Add route in `app.py`
2. Create template in `templates/`
3. Add navigation link in `dashboard.html`
4. Consider if new progress tracking table is needed in `models.py`

## Security Considerations

- **Local network only** - No HTTPS, simple passwords, hardcoded secret key
- **Not for production** - Auth is intentionally simple for family use
- If exposing to internet: Implement proper password hashing, HTTPS, CSRF protection, input validation

## Deployment (Raspberry Pi)

- App runs on `0.0.0.0:8000` by default (all network interfaces)
- Port 8000 chosen to avoid conflicts with macOS AirPlay Receiver (which uses 5000)
- Debug mode enabled - disable for production by changing `debug=False` in `app.py`
- Consider using systemd service for auto-start on boot
- SQLite database is file-based, no separate DB server needed
