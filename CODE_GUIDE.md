# Code Guide - Learn German App

This document explains the architecture and how the code works.

## Table of Contents

1. [Application Architecture](#application-architecture)
2. [Database Models](#database-models)
3. [Core Application Flow](#core-application-flow)
4. [Key Features Implementation](#key-features-implementation)
5. [Frontend Integration](#frontend-integration)

---

## Application Architecture

### Technology Stack

- **Flask**: Web framework handling routing, sessions, and HTTP requests
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database stored in `instance/learnGerman.db`
- **Bootstrap 5**: CSS framework for responsive UI
- **Chart.js**: JavaScript library for progress visualization
- **Jinja2**: Template engine (built into Flask)

### File Structure

```
app.py              # Main Flask application (routes, logic)
models.py           # Database models (ORM)
init_db.py          # Database initialization script
templates/          # Jinja2 HTML templates
instance/           # Flask instance folder (database)
```

---

## Database Models

All models are defined in `models.py` using SQLAlchemy ORM.

### User Model
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
```

Stores user credentials. Currently 3 users: sam, sheryl, chris.

### Word Model
```python
class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    german = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100), nullable=False)
    article = db.Column(db.String(10))  # der, die, das
```

Stores German nouns with their English translations and grammatical articles.

### Verb Model
```python
class Verb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    infinitive = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100), nullable=False)
    ich = db.Column(db.String(100))
    du = db.Column(db.String(100))
    er_sie_es = db.Column(db.String(100))
    wir = db.Column(db.String(100))
    ihr = db.Column(db.String(100))
    sie_Sie = db.Column(db.String(100))
```

Stores German verbs with all present tense conjugations.

### Progress Tracking Models

**UserProgress**: Overall stats per user
```python
class UserProgress(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_time_minutes = db.Column(db.Integer, default=0)
    words_learned = db.Column(db.Integer, default=0)
    verbs_learned = db.Column(db.Integer, default=0)
```

**WordProgress**: Per-word tracking
```python
class WordProgress(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
    times_seen = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)
    times_incorrect = db.Column(db.Integer, default=0)
    last_seen = db.Column(db.DateTime)
```

**VerbProgress**: Per-verb tracking (same structure as WordProgress)

### Test Models

**TestResult**: Test scores and metadata
```python
class TestResult(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    test_type = db.Column(db.String(20))  # 'vocabulary' or 'verb'
    is_mock = db.Column(db.Boolean)
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    percentage = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
```

**TestAnswer**: Individual test question answers
```python
class TestAnswer(db.Model):
    test_result_id = db.Column(db.Integer, db.ForeignKey('test_result.id'))
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=True)
    verb_id = db.Column(db.Integer, db.ForeignKey('verb.id'), nullable=True)
    user_answer = db.Column(db.String(200))
    is_correct = db.Column(db.Boolean)
```

### Activity Tracking

**ActivityLog**: Session time tracking
```python
class ActivityLog(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
```

---

## Core Application Flow

### 1. Authentication (`app.py:20-60`)

**Login Route** (`/login`)
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            session['username'] = username
            session['last_activity'] = datetime.utcnow().isoformat()
            return redirect(url_for('dashboard'))
```

Simple credential check - no hashing (local network only).

**Session Management**
- Flask session stores: `user_id`, `username`, `last_activity`
- Session persists across requests
- Logout clears session

### 2. Activity Tracking (`app.py:62-95`)

**Middleware Hook**
```python
@app.before_request
def before_request():
    if request.endpoint not in ['login', 'static'] and 'user_id' in session:
        update_activity()
```

Runs before every request to track user activity.

**Activity Update Logic**
```python
def update_activity():
    now = datetime.utcnow()
    last_activity = datetime.fromisoformat(session['last_activity'])

    # Check if more than 5 minutes inactive
    if (now - last_activity).total_seconds() > 300:
        # End previous session, start new one
        end_last_activity()
        start_new_activity()
    else:
        # Continue current session
        session['last_activity'] = now.isoformat()
```

**Session Ending**
```python
def end_last_activity():
    # Find most recent activity log without end_time
    activity = ActivityLog.query.filter_by(
        user_id=session['user_id'],
        end_time=None
    ).order_by(ActivityLog.start_time.desc()).first()

    if activity:
        activity.end_time = datetime.fromisoformat(session['last_activity'])
        duration = (activity.end_time - activity.start_time).total_seconds() / 60
        activity.duration_minutes = int(duration)

        # Update user's total time
        user_progress.total_time_minutes += int(duration)
```

### 3. Smart Content Selection Algorithm (`app.py:150-180`)

Used in vocabulary and verb learning to prioritize challenging items.

```python
def get_next_word(user_id):
    # Get all words the user has seen
    progress_records = WordProgress.query.filter_by(user_id=user_id).all()
    seen_word_ids = [p.word_id for p in progress_records]

    # Priority 1: Unseen words
    unseen_words = Word.query.filter(~Word.id.in_(seen_word_ids)).all()
    if unseen_words:
        return random.choice(unseen_words)

    # Priority 2: Words with more incorrect than correct
    struggling_progress = [p for p in progress_records
                          if p.times_incorrect > p.times_correct]
    if struggling_progress:
        progress = random.choice(struggling_progress)
        return Word.query.get(progress.word_id)

    # Priority 3: Random word
    return random.choice(Word.query.all())
```

This ensures users see new content first, then practice what they struggle with.

---

## Key Features Implementation

### Vocabulary Learning (`app.py:200-270`)

**Route: `/learn-vocabulary`**

1. Get next word using smart selection
2. Create or retrieve WordProgress record
3. Display word in template
4. Track "seen" count on page load

**Route: `/mark-word-answer` (POST)**

Handles user marking correct/incorrect:

```python
@app.route('/mark-word-answer', methods=['POST'])
def mark_word_answer():
    word_id = request.form['word_id']
    is_correct = request.form['is_correct'] == 'true'

    # Update or create progress record
    progress = WordProgress.query.filter_by(
        user_id=session['user_id'],
        word_id=word_id
    ).first()

    if not progress:
        progress = WordProgress(
            user_id=session['user_id'],
            word_id=word_id,
            times_seen=1,  # Explicitly set to avoid None
            times_correct=0,
            times_incorrect=0
        )
        db.session.add(progress)

    # Update counts
    if is_correct:
        progress.times_correct += 1
    else:
        progress.times_incorrect += 1

    progress.last_seen = datetime.utcnow()
    db.session.commit()

    # Update user's words_learned count
    update_words_learned_count(session['user_id'])
```

**Critical Fix**: Explicitly setting default values (times_seen=0, etc.) was necessary because SQLAlchemy wasn't applying model defaults properly, causing `NoneType + int` errors.

### Verb Practice (`app.py:272-350`)

Similar to vocabulary but with conjugation checking:

```python
@app.route('/check-verb', methods=['POST'])
def check_verb():
    verb_id = session.get('current_verb_id')
    verb = Verb.query.get(verb_id)

    # Get user's conjugations
    user_conjugations = {
        'ich': request.form.get('ich', '').strip().lower(),
        'du': request.form.get('du', '').strip().lower(),
        # ... etc
    }

    # Compare with correct conjugations
    correct_conjugations = {
        'ich': verb.ich.lower(),
        'du': verb.du.lower(),
        # ... etc
    }

    is_perfect = user_conjugations == correct_conjugations

    # Calculate score (how many were correct)
    correct_count = sum(1 for k in user_conjugations
                       if user_conjugations[k] == correct_conjugations[k])
```

### Mock Tests (`app.py:400-480`)

**Flow:**

1. **Start Test** (`/mock-test/<type>/<direction>?restart=1`)
   - Randomly select 10 words/verbs
   - Store in session: `test_questions`, `test_current`, `test_score`, `test_type`, `test_direction`

2. **Display Question** (`/mock-test/<type>/<direction>`)
   - Show question based on direction (de-en or en-de)
   - For vocabulary: Show article + word or English
   - For verbs: Show infinitive or English

3. **Submit Answer** (`/submit-mock-answer` POST)
   - Validate answer with flexible matching
   - Return JSON: `{is_correct, correct_answer, has_more}`

4. **Validation Logic**:
```python
if direction == 'de-en':
    # German to English
    correct_answer = word.english.lower()
    user_answer = request.form['answer'].strip().lower()

    # Accept with or without "the"
    is_correct = (user_answer == correct_answer or
                 user_answer == 'the ' + correct_answer or
                 'the ' + user_answer == correct_answer)
else:
    # English to German
    correct_answer = word.german.lower()
    correct_with_article = (word.article + ' ' + word.german).lower()

    # Accept with or without article
    is_correct = (user_answer == correct_answer or
                 user_answer == correct_with_article)
```

5. **Save Results** (`/test-complete`)
   - Create TestResult record
   - Create TestAnswer records for each question
   - Calculate percentage
   - Clear session test data

### Real Tests (`app.py:485-560`)

Same structure as mock tests but:
- Always English ’ German direction
- 20 questions instead of 10
- No instant feedback (all feedback at end)
- Grade calculation:
```python
def get_letter_grade(percentage):
    if percentage >= 90: return 'A'
    elif percentage >= 80: return 'B'
    elif percentage >= 70: return 'C'
    elif percentage >= 60: return 'D'
    else: return 'F'
```

### Progress Page (`app.py:565-620`)

**Route: `/progress`**

Aggregates and displays:

```python
def progress():
    user_progress = UserProgress.query.filter_by(user_id=session['user_id']).first()

    # Get test results
    test_results = TestResult.query.filter_by(
        user_id=session['user_id']
    ).order_by(TestResult.date.desc()).all()

    # Calculate totals
    total_words = Word.query.count()
    total_verbs = Verb.query.count()

    # Get trending data for charts
    recent_tests = test_results[:10]  # Last 10 tests

    return render_template('progress.html',
        progress=user_progress,
        total_words=total_words,
        total_verbs=total_verbs,
        test_results=test_results,
        recent_tests=recent_tests
    )
```

**Progress Bar Calculation** (in template):
```html
{{ ((progress.words_learned / total_words * 100)|round(1)) if total_words > 0 else 0 }}%
```

---

## Frontend Integration

### Template Inheritance

**base.html**: Master template
- Navigation bar
- User info display
- Logout button
- Blue gradient background CSS
- JetBrains Mono font
- Bootstrap 5 CSS

All other templates extend base:
```html
{% extends "base.html" %}
{% block title %}Page Title{% endblock %}
{% block content %}
  <!-- Page content -->
{% endblock %}
```

### AJAX for Tests (`templates/mock_test.html`)

**Form Submission**:
```javascript
function submitAnswer(event) {
    event.preventDefault();
    const formData = new FormData(form);

    fetch('/submit-mock-answer', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Display feedback
        if (data.is_correct) {
            // Show success message
        } else {
            // Show correct answer
        }

        if (data.has_more) {
            // Show "Next Question" button
        } else {
            // Show "Finish Test" button
        }
    });
}
```

**Enter Key Support**:
```javascript
function handleEnterKey(e) {
    if (e.key === 'Enter') {
        document.removeEventListener('keypress', handleEnterKey);
        const nextBtn = document.getElementById('nextBtn');
        if (nextBtn) {
            nextBtn.click();
        }
    }
}

// Add listener after feedback is shown
document.getElementById('nextBtn').focus();
document.addEventListener('keypress', handleEnterKey);
```

### Chart.js Integration (`templates/progress.html`)

```html
<canvas id="testTrendChart"></canvas>

<script>
const ctx = document.getElementById('testTrendChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: {{ test_dates | tojson }},
        datasets: [{
            label: 'Test Scores (%)',
            data: {{ test_scores | tojson }},
            borderColor: '#0066cc',
            backgroundColor: 'rgba(0, 102, 204, 0.1)',
        }]
    }
});
</script>
```

---

## Important Implementation Notes

### Database Default Values Bug

Original model definitions had default values:
```python
times_seen = db.Column(db.Integer, default=0)
```

But SQLAlchemy wasn't applying them during record creation, causing `None + int` errors.

**Solution**: Explicitly set values in code:
```python
progress = WordProgress(
    user_id=session['user_id'],
    word_id=word_id,
    times_seen=0,
    times_correct=0,
    times_incorrect=0
)
```

### Foreign Key Cascade Deletion

When deleting words, must delete related records first:
```python
# 1. Delete WordProgress records
WordProgress.query.filter(
    WordProgress.word_id.in_(word_ids_to_delete)
).delete(synchronize_session='fetch')

# 2. Delete TestAnswer records
TestAnswer.query.filter(
    TestAnswer.word_id.in_(word_ids_to_delete)
).delete(synchronize_session='fetch')

# 3. Finally delete Word records
Word.query.filter(Word.id > 105).delete()
```

### Session State Management

Test state stored in Flask session:
```python
session['test_questions'] = [1, 5, 8, 12, ...]  # IDs
session['test_current'] = 0  # Current question index
session['test_score'] = 0
session['test_type'] = 'vocabulary'
session['test_direction'] = 'de-en'
```

Session is cleared after test completion to prevent stale data.

### Activity Tracking Edge Cases

- First login: Create new ActivityLog entry
- Page refresh within 5 minutes: Update last_activity timestamp
- Inactivity > 5 minutes: End previous session, start new one
- Logout: End current session, calculate duration

---

## Development Tips

### Adding New Words/Verbs

1. Check for duplicates:
```python
existing = Word.query.filter_by(german=german).first()
if not existing:
    # Add new word
```

2. Commit after adding:
```python
db.session.add(word)
db.session.commit()
```

### Debugging Database Issues

Enable SQL echo:
```python
app.config['SQLALCHEMY_ECHO'] = True
```

Check database directly:
```bash
sqlite3 instance/learnGerman.db
.tables
SELECT * FROM word LIMIT 10;
```

### Testing Without Browser

Use Flask test client:
```python
with app.test_client() as client:
    response = client.post('/login', data={'username': 'sam', 'password': 'sam'})
    assert response.status_code == 302  # Redirect
```

---

## Configuration Reference

### Flask App Config (`app.py:5-15`)

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnGerman.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

### Running Configuration (`app.py:~500`)

```python
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',  # Allow network access
        port=8000,        # Avoid macOS AirPlay port 5000
        debug=True        # Enable auto-reload and error pages
    )
```

---

## Common Modifications

### Change Test Question Count

Mock tests: Modify line ~405
```python
num_questions = 10  # Change to desired number
```

Real tests: Modify line ~490
```python
num_questions = 20  # Change to desired number
```

### Change Inactivity Timeout

Modify line ~75
```python
if (now - last_activity).total_seconds() > 300:  # 300 = 5 minutes
```

### Adjust Grading Scale

Modify `get_letter_grade()` function around line ~550
```python
if percentage >= 95: return 'A'  # Make A harder to get
```

### Add New User

In `init_db.py`, add to users list:
```python
users = [
    User(username='sam', password='sam'),
    User(username='sheryl', password='sheryl'),
    User(username='chris', password='chris'),
    User(username='newuser', password='newuser'),  # Add here
]
```

Then reinitialize database or manually add via SQLite.

---

This guide covers the main architecture and implementation details. For specific questions, refer to inline comments in `app.py` and `models.py`.
