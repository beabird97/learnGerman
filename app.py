from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from models import db, User, Word, Verb, UserProgress, WordProgress, VerbProgress, TestResult, TestAnswer, ActivityLog
from datetime import datetime, timedelta
from functools import wraps
import random
import csv
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'learn-german-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learnGerman.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Custom Jinja filter for timezone adjustment (UTC to local time, +1 hour for CET/CEST)
@app.template_filter('localtime')
def localtime_filter(dt):
    """Convert UTC datetime to local time (CET/CEST, +1 hour)"""
    if dt is None:
        return None
    return dt + timedelta(hours=1)

# Helper function to normalize umlauts for answer comparison
def normalize_umlauts(text):
    """Convert umlauts to their ae/oe/ue/ss equivalents for flexible answer matching"""
    if not text:
        return text
    replacements = {
        'ä': 'ae', 'Ä': 'Ae',
        'ö': 'oe', 'Ö': 'Oe',
        'ü': 'ue', 'Ü': 'Ue',
        'ß': 'ss'
    }
    normalized = text
    for umlaut, replacement in replacements.items():
        normalized = normalized.replace(umlaut, replacement)
    return normalized

# Helper function to get face and comment based on score
def get_face_and_comment(percentage):
    """Return face filename and snarky comment based on test performance"""
    if percentage >= 90:
        comments = [
            "Outstanding! You're practically fluent already!",
            "Perfekt! Are you secretly German?",
            "Wow! You crushed it! 🎉",
            "Incredible! You're ready to move to Berlin!",
            "Flawless victory! The German language fears you!"
        ]
        return 'face4.bmp', random.choice(comments)
    elif percentage >= 80:
        comments = [
            "Great job! Keep up the excellent work!",
            "Sehr gut! You're doing amazing!",
            "Impressive! Almost perfect!",
            "Wunderbar! You know your stuff!",
            "Excellent work! Just a few more practice rounds!"
        ]
        return 'face3.bmp', random.choice(comments)
    elif percentage >= 70:
        comments = [
            "Pretty good! You're getting there!",
            "Not bad at all! Keep practicing!",
            "Solid effort! You're on the right track!",
            "Respectable score! A bit more study and you'll ace it!",
            "Nice work! You're making real progress!"
        ]
        return 'face1.bmp', random.choice(comments)
    elif percentage >= 60:
        comments = [
            "Not bad, but there's room for improvement.",
            "Passing grade, but you can do better.",
            "Meh. It's okay, I guess.",
            "Average performance. Time to step it up!",
            "You passed, but let's aim higher next time."
        ]
        return 'face8.bmp', random.choice(comments)
    elif percentage >= 50:
        comments = [
            "Hmm... maybe review those flashcards again?",
            "Slightly below average. Did you study?",
            "Oof. That's barely passing territory.",
            "I've seen better. Back to the drawing board!",
            "Not great, not terrible. Actually, kind of terrible."
        ]
        return 'face0.bmp', random.choice(comments)
    elif percentage >= 40:
        comments = [
            "Ouch. Time to hit the books!",
            "This is painful to watch. More practice needed!",
            "Disappointing! Were the umlauts confusing you?",
            "Yikes. Let's pretend this didn't happen.",
            "That's... not good. Like, at all."
        ]
        return 'face7.bmp', random.choice(comments)
    elif percentage >= 30:
        comments = [
            "Yikes! Were you even paying attention?",
            "Terrible! Did you study the wrong language?",
            "This is bad. Really bad.",
            "I'm not angry, just disappointed. Actually, I'm both.",
            "Are you allergic to correct answers?"
        ]
        return 'face9.bmp', random.choice(comments)
    else:
        comments = [
            "Did you just randomly guess everything?",
            "This is catastrophic. Were you blindfolded?",
            "I don't even know what to say. Wow.",
            "Please tell me this was a joke attempt.",
            "The textbook is crying right now.",
            "Maybe try a different language? Like English?",
            "This score is actually impressive... impressively bad."
        ]
        return 'face5.bmp', random.choice(comments)

# Activity tracking helper
def update_activity():
    if 'user_id' in session and 'last_activity' in session:
        last_activity = datetime.fromisoformat(session['last_activity'])
        now = datetime.utcnow()

        # If more than 5 minutes of inactivity, start new session
        if (now - last_activity).total_seconds() > 300:  # 5 minutes
            # End previous activity log
            if 'activity_log_id' in session:
                log = ActivityLog.query.get(session['activity_log_id'])
                if log and not log.end_time:
                    log.end_time = last_activity
                    log.duration_minutes = int((log.end_time - log.start_time).total_seconds() / 60)

                    # Update user's total time
                    progress = UserProgress.query.filter_by(user_id=session['user_id']).first()
                    if progress:
                        progress.total_time_minutes += log.duration_minutes
                    db.session.commit()

            # Start new activity log
            new_log = ActivityLog(user_id=session['user_id'])
            db.session.add(new_log)
            db.session.commit()
            session['activity_log_id'] = new_log.id

        session['last_activity'] = now.isoformat()

def start_activity_tracking():
    if 'user_id' in session:
        log = ActivityLog(user_id=session['user_id'])
        db.session.add(log)
        db.session.commit()
        session['activity_log_id'] = log.id
        session['last_activity'] = datetime.utcnow().isoformat()

def end_activity_tracking():
    if 'activity_log_id' in session:
        log = ActivityLog.query.get(session['activity_log_id'])
        if log and not log.end_time:
            log.end_time = datetime.utcnow()
            log.duration_minutes = int((log.end_time - log.start_time).total_seconds() / 60)

            # Update user's total time
            progress = UserProgress.query.filter_by(user_id=session['user_id']).first()
            if progress:
                progress.total_time_minutes += log.duration_minutes
            db.session.commit()

# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('You need admin privileges to access this page.')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def before_request():
    if request.endpoint not in ['login', 'static'] and 'user_id' in session:
        update_activity()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            start_activity_tracking()
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    end_activity_tracking()
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    is_admin = user.is_admin if user else False
    return render_template('dashboard.html', username=session['username'], is_admin=is_admin)

@app.route('/mock-test-selection')
def mock_test_selection():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('mock_test_selection.html')

@app.route('/real-test-selection')
def real_test_selection():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('real_test_selection.html')

@app.route('/progress')
def progress():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_progress = UserProgress.query.filter_by(user_id=session['user_id']).first()

    # Calculate total time including current session
    total_time = user_progress.total_time_minutes if user_progress else 0

    # Add current session time if there's an active session
    if 'activity_log_id' in session:
        current_log = ActivityLog.query.get(session['activity_log_id'])
        if current_log and not current_log.end_time:
            current_duration = int((datetime.utcnow() - current_log.start_time).total_seconds() / 60)
            total_time += current_duration

    # Calculate today's learning time
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_logs = ActivityLog.query.filter(
        ActivityLog.user_id == session['user_id'],
        ActivityLog.start_time >= today_start
    ).all()

    today_time = 0
    for log in today_logs:
        if log.end_time:
            # Completed session
            today_time += log.duration_minutes
        elif 'activity_log_id' in session and log.id == session['activity_log_id']:
            # Current active session
            current_duration = int((datetime.utcnow() - log.start_time).total_seconds() / 60)
            today_time += current_duration

    # Get all test results
    real_tests = TestResult.query.filter_by(user_id=session['user_id'], is_mock=False).order_by(TestResult.date.desc()).all()

    # Get wrong answers for each real test
    real_tests_with_mistakes = []
    for test in real_tests:
        wrong_answers = TestAnswer.query.filter_by(test_id=test.id, is_correct=False).all()
        mistakes = []
        for answer in wrong_answers:
            if answer.word_id:
                word = Word.query.get(answer.word_id)
                if word:
                    mistakes.append(f"{word.article} {word.german}")
            elif answer.verb_id:
                verb = Verb.query.get(answer.verb_id)
                if verb:
                    mistakes.append(verb.infinitive)
        real_tests_with_mistakes.append({
            'test': test,
            'mistakes': mistakes
        })

    # Get mock test results for trending
    mock_tests_raw = TestResult.query.filter_by(user_id=session['user_id'], is_mock=True).order_by(TestResult.date.desc()).limit(10).all()

    # Get wrong answers for each mock test (if they have TestAnswer records)
    mock_tests_with_mistakes = []
    for test in mock_tests_raw:
        wrong_answers = TestAnswer.query.filter_by(test_id=test.id, is_correct=False).all()
        mistakes = []
        for answer in wrong_answers:
            if answer.word_id:
                word = Word.query.get(answer.word_id)
                if word:
                    mistakes.append(f"{word.article} {word.german}")
            elif answer.verb_id:
                verb = Verb.query.get(answer.verb_id)
                if verb:
                    mistakes.append(verb.infinitive)
        mock_tests_with_mistakes.append({
            'test': test,
            'mistakes': mistakes
        })

    # Get totals for progress bars
    total_words = Word.query.count()
    total_verbs = Verb.query.count()

    return render_template('progress.html',
                         progress=user_progress,
                         total_time=total_time,
                         today_time=today_time,
                         real_tests=real_tests_with_mistakes,
                         mock_tests=mock_tests_with_mistakes,
                         total_words=total_words,
                         total_verbs=total_verbs)

@app.route('/clear-mock-tests', methods=['POST'])
def clear_mock_tests():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    # Delete all mock test results for this user
    TestResult.query.filter_by(user_id=session['user_id'], is_mock=True).delete()
    db.session.commit()

    return '', 204

@app.route('/learn-vocabulary')
def learn_vocabulary():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get all words and their progress
    all_words = Word.query.all()
    user_progress = WordProgress.query.filter_by(user_id=session['user_id']).all()
    progress_dict = {p.word_id: p for p in user_progress}

    # Build weighted selection list based on priority_score
    # Unseen words get default score (100.0), seen words use their priority_score
    word_weights = []
    for word in all_words:
        if word.id not in progress_dict:
            # Unseen word - highest priority
            weight = 100.0
        else:
            # Use the stored priority_score
            weight = progress_dict[word.id].priority_score or 100.0
        word_weights.append((word, weight))

    # Weighted random selection
    if word_weights:
        words, weights = zip(*word_weights)
        selected_word = random.choices(words, weights=weights, k=1)[0]
    else:
        selected_word = None

    return render_template('learn_vocabulary.html', word=selected_word)

@app.route('/mark-word-learned/<int:word_id>')
def mark_word_learned(word_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    progress = WordProgress.query.filter_by(user_id=session['user_id'], word_id=word_id).first()
    if not progress:
        progress = WordProgress(
            user_id=session['user_id'],
            word_id=word_id,
            times_seen=0,
            times_correct=0,
            times_incorrect=0
        )
        db.session.add(progress)

    progress.times_seen += 1
    progress.last_seen = datetime.utcnow()

    # Update user's total words learned count
    user_progress = UserProgress.query.filter_by(user_id=session['user_id']).first()
    if user_progress:
        # Count unique words seen by this user
        words_seen = WordProgress.query.filter_by(user_id=session['user_id']).filter(WordProgress.times_seen > 0).count()
        user_progress.words_learned = words_seen

    db.session.commit()

    return redirect(url_for('learn_vocabulary'))

@app.route('/check-word/<int:word_id>', methods=['POST'])
def check_word(word_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    word = Word.query.get_or_404(word_id)
    user_answer = request.form.get('answer', '').strip()

    # Check answer with article flexibility and umlaut substitutions
    correct_answer = word.german
    correct_with_article = word.article + ' ' + word.german

    # Normalize for umlaut substitutions
    user_normalized = normalize_umlauts(user_answer.lower())
    correct_normalized = normalize_umlauts(correct_answer.lower())
    correct_with_article_normalized = normalize_umlauts(correct_with_article.lower())

    # Accept with or without article
    is_correct = (user_normalized == correct_normalized or
                 user_normalized == correct_with_article_normalized)

    # Update progress
    progress = WordProgress.query.filter_by(user_id=session['user_id'], word_id=word_id).first()
    if not progress:
        progress = WordProgress(
            user_id=session['user_id'],
            word_id=word_id,
            times_seen=0,
            times_correct=0,
            times_incorrect=0
        )
        db.session.add(progress)

    progress.times_seen += 1
    if is_correct:
        progress.times_correct += 1
        # Decrease priority score when correct (make less likely to appear)
        current_score = progress.priority_score if progress.priority_score is not None else 100.0
        progress.priority_score = max(1.0, current_score * 0.7)
    else:
        progress.times_incorrect += 1
        # Increase priority score when incorrect (make more likely to appear)
        current_score = progress.priority_score if progress.priority_score is not None else 100.0
        progress.priority_score = min(200.0, current_score * 1.5)
    progress.last_seen = datetime.utcnow()

    # Update user's total words learned count
    user_progress = UserProgress.query.filter_by(user_id=session['user_id']).first()
    if user_progress:
        # Count unique words seen by this user
        words_seen = WordProgress.query.filter_by(user_id=session['user_id']).filter(WordProgress.times_seen > 0).count()
        user_progress.words_learned = words_seen

    db.session.commit()

    return jsonify({
        'is_correct': is_correct,
        'user_answer': user_answer,
        'correct_answer': correct_with_article,
        'english': word.english
    })

@app.route('/learn-verbs')
def learn_verbs():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get all verbs and their progress
    all_verbs = Verb.query.all()
    user_progress = VerbProgress.query.filter_by(user_id=session['user_id']).all()
    progress_dict = {p.verb_id: p for p in user_progress}

    # Build weighted selection list based on priority_score
    verb_weights = []
    for verb in all_verbs:
        if verb.id not in progress_dict:
            # Unseen verb - highest priority
            weight = 100.0
        else:
            # Use the stored priority_score
            weight = progress_dict[verb.id].priority_score or 100.0
        verb_weights.append((verb, weight))

    # Weighted random selection
    if verb_weights:
        verbs, weights = zip(*verb_weights)
        selected_verb = random.choices(verbs, weights=weights, k=1)[0]
    else:
        selected_verb = None

    return render_template('learn_verbs.html', verb=selected_verb)

@app.route('/check-verb/<int:verb_id>', methods=['POST'])
def check_verb(verb_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    verb = Verb.query.get_or_404(verb_id)

    user_answers = {
        'ich': request.form.get('ich', '').strip().lower(),
        'du': request.form.get('du', '').strip().lower(),
        'er_sie_es': request.form.get('er_sie_es', '').strip().lower(),
        'wir': request.form.get('wir', '').strip().lower(),
        'ihr': request.form.get('ihr', '').strip().lower(),
        'sie_Sie': request.form.get('sie_Sie', '').strip().lower()
    }

    correct_answers = {
        'ich': verb.ich.lower(),
        'du': verb.du.lower(),
        'er_sie_es': verb.er_sie_es.lower(),
        'wir': verb.wir.lower(),
        'ihr': verb.ihr.lower(),
        'sie_Sie': verb.sie_Sie.lower()
    }

    results = {}
    all_correct = True
    for key in user_answers:
        is_correct = user_answers[key] == correct_answers[key]
        results[key] = {
            'correct': is_correct,
            'user_answer': user_answers[key],
            'correct_answer': correct_answers[key]
        }
        if not is_correct:
            all_correct = False

    # Update progress
    progress = VerbProgress.query.filter_by(user_id=session['user_id'], verb_id=verb_id).first()
    if not progress:
        progress = VerbProgress(
            user_id=session['user_id'],
            verb_id=verb_id,
            times_seen=0,
            times_correct=0,
            times_incorrect=0
        )
        db.session.add(progress)

    progress.times_seen += 1
    if all_correct:
        progress.times_correct += 1
        # Decrease priority score when correct (make less likely to appear)
        current_score = progress.priority_score if progress.priority_score is not None else 100.0
        progress.priority_score = max(1.0, current_score * 0.7)
    else:
        progress.times_incorrect += 1
        # Increase priority score when incorrect (make more likely to appear)
        current_score = progress.priority_score if progress.priority_score is not None else 100.0
        progress.priority_score = min(200.0, current_score * 1.5)
    progress.last_seen = datetime.utcnow()

    # Update user's total verbs learned count
    user_progress = UserProgress.query.filter_by(user_id=session['user_id']).first()
    if user_progress:
        # Count unique verbs seen by this user
        verbs_seen = VerbProgress.query.filter_by(user_id=session['user_id']).filter(VerbProgress.times_seen > 0).count()
        user_progress.verbs_learned = verbs_seen

    db.session.commit()

    return jsonify({'results': results, 'all_correct': all_correct})

@app.route('/mock-test/<test_type>/<direction>')
def mock_test(test_type, direction):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if test_type not in ['vocabulary', 'verb']:
        return redirect(url_for('dashboard'))

    if direction not in ['de-en', 'en-de']:
        return redirect(url_for('dashboard'))

    # Initialize test session
    if 'test_questions' not in session or request.args.get('restart'):
        session['test_type'] = test_type
        session['test_direction'] = direction
        session['is_mock'] = True
        session['current_question'] = 0
        session['test_score'] = 0

        if test_type == 'vocabulary':
            # Use weighted selection based on priority_score
            all_words = Word.query.all()
            user_progress = WordProgress.query.filter_by(user_id=session['user_id']).all()
            progress_dict = {p.word_id: p for p in user_progress}

            word_weights = []
            for word in all_words:
                weight = progress_dict[word.id].priority_score if word.id in progress_dict else 100.0
                word_weights.append((word, weight))

            if word_weights:
                words, weights = zip(*word_weights)
                selected_words = random.choices(words, weights=weights, k=min(10, len(words)))
                session['test_questions'] = [w.id for w in selected_words]
            else:
                session['test_questions'] = []
        else:
            # Use weighted selection for verbs
            all_verbs = Verb.query.all()
            user_progress = VerbProgress.query.filter_by(user_id=session['user_id']).all()
            progress_dict = {p.verb_id: p for p in user_progress}

            verb_weights = []
            for verb in all_verbs:
                weight = progress_dict[verb.id].priority_score if verb.id in progress_dict else 100.0
                verb_weights.append((verb, weight))

            if verb_weights:
                verbs, weights = zip(*verb_weights)
                selected_verbs = random.choices(verbs, weights=weights, k=min(4, len(verbs)))
                session['test_questions'] = [v.id for v in selected_verbs]
            else:
                session['test_questions'] = []

    if session['current_question'] >= len(session['test_questions']):
        return redirect(url_for('test_complete'))

    question_id = session['test_questions'][session['current_question']]

    if test_type == 'vocabulary':
        question = Word.query.get(question_id)
    else:
        question = Verb.query.get(question_id)

    return render_template('mock_test.html',
                         question=question,
                         test_type=test_type,
                         direction=direction,
                         question_num=session['current_question'] + 1,
                         total=len(session['test_questions']))

@app.route('/submit-mock-answer', methods=['POST'])
def submit_mock_answer():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    test_type = session.get('test_type')
    direction = session.get('test_direction', 'de-en')
    question_id = session['test_questions'][session['current_question']]

    if test_type == 'vocabulary':
        word = Word.query.get(question_id)
        user_answer = request.form.get('answer', '').strip().lower()

        if direction == 'de-en':
            # German to English - accept with or without "the"
            correct_answer = word.english.lower()
            # Check if answer matches with or without article
            is_correct = (user_answer == correct_answer or
                         user_answer == 'the ' + correct_answer or
                         'the ' + user_answer == correct_answer)
        else:
            # English to German - accept with or without article and with umlaut substitutions
            # For comparison, use lowercase
            correct_answer_compare = word.german.lower()
            correct_with_article_compare = (word.article + ' ' + word.german).lower()

            # Normalize both user answer and correct answers for comparison
            user_normalized = normalize_umlauts(user_answer)
            correct_normalized = normalize_umlauts(correct_answer_compare)
            correct_with_article_normalized = normalize_umlauts(correct_with_article_compare)

            is_correct = (user_normalized == correct_normalized or
                         user_normalized == correct_with_article_normalized)
            # For display purposes, show the version with article and proper capitalization
            correct_answer = word.article + ' ' + word.german

        # Update progress
        progress = WordProgress.query.filter_by(user_id=session['user_id'], word_id=word.id).first()
        if not progress:
            progress = WordProgress(
                user_id=session['user_id'],
                word_id=word.id,
                times_seen=0,
                times_correct=0,
                times_incorrect=0
            )
            db.session.add(progress)

        progress.times_seen += 1
        if is_correct:
            progress.times_correct += 1
            session['test_score'] += 1
            # Decrease priority score when correct
            current_score = progress.priority_score if progress.priority_score is not None else 100.0
            progress.priority_score = max(1.0, current_score * 0.7)
        else:
            progress.times_incorrect += 1
            # Increase priority score when incorrect
            current_score = progress.priority_score if progress.priority_score is not None else 100.0
            progress.priority_score = min(200.0, current_score * 1.5)
        progress.last_seen = datetime.utcnow()

    else:  # verb test - check all conjugations
        verb = Verb.query.get(question_id)

        # Get all 6 conjugation answers
        conjugations = ['ich', 'du', 'er_sie_es', 'wir', 'ihr', 'sie_Sie']
        results = {}
        correct_count = 0

        for conj in conjugations:
            user_answer = request.form.get(conj, '').strip().lower()
            correct_answer = getattr(verb, conj).lower()

            # Normalize for umlaut substitutions
            user_normalized = normalize_umlauts(user_answer)
            correct_normalized = normalize_umlauts(correct_answer)

            is_correct = user_normalized == correct_normalized
            if is_correct:
                correct_count += 1

            results[conj] = {
                'correct': is_correct,
                'user_answer': user_answer,
                'correct_answer': getattr(verb, conj)
            }

        # Update progress
        progress = VerbProgress.query.filter_by(user_id=session['user_id'], verb_id=verb.id).first()
        if not progress:
            progress = VerbProgress(
                user_id=session['user_id'],
                verb_id=verb.id,
                times_seen=0,
                times_correct=0,
                times_incorrect=0
            )
            db.session.add(progress)

        progress.times_seen += 1
        # Count as correct only if all 6 are correct
        all_correct = correct_count == 6
        if all_correct:
            progress.times_correct += 1
            # Decrease priority score when correct
            current_score = progress.priority_score if progress.priority_score is not None else 100.0
            progress.priority_score = max(1.0, current_score * 0.7)
        else:
            progress.times_incorrect += 1
            # Increase priority score when incorrect
            current_score = progress.priority_score if progress.priority_score is not None else 100.0
            progress.priority_score = min(200.0, current_score * 1.5)
        progress.last_seen = datetime.utcnow()

        # Add partial credit to score (each conjugation = 1/6 point)
        session['test_score'] += correct_count / 6

    db.session.commit()

    session['current_question'] += 1

    # Return different format for verbs (with results) vs vocabulary
    if test_type == 'verb':
        return jsonify({
            'results': results,
            'has_more': session['current_question'] < len(session['test_questions'])
        })
    else:
        return jsonify({
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'has_more': session['current_question'] < len(session['test_questions'])
        })

@app.route('/real-test/<test_type>')
def real_test(test_type):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if test_type not in ['vocabulary', 'verb']:
        return redirect(url_for('dashboard'))

    # Initialize test session
    if 'test_questions' not in session or request.args.get('restart'):
        session['test_type'] = test_type
        session['is_mock'] = False
        session['current_question'] = 0
        session['test_answers'] = []

        if test_type == 'vocabulary':
            # Use weighted selection based on priority_score
            all_words = Word.query.all()
            user_progress = WordProgress.query.filter_by(user_id=session['user_id']).all()
            progress_dict = {p.word_id: p for p in user_progress}

            word_weights = []
            for word in all_words:
                weight = progress_dict[word.id].priority_score if word.id in progress_dict else 100.0
                word_weights.append((word, weight))

            if word_weights:
                words, weights = zip(*word_weights)
                selected_words = random.choices(words, weights=weights, k=min(20, len(words)))
                session['test_questions'] = [w.id for w in selected_words]
            else:
                session['test_questions'] = []
        else:
            # Use weighted selection for verbs
            all_verbs = Verb.query.all()
            user_progress = VerbProgress.query.filter_by(user_id=session['user_id']).all()
            progress_dict = {p.verb_id: p for p in user_progress}

            verb_weights = []
            for verb in all_verbs:
                weight = progress_dict[verb.id].priority_score if verb.id in progress_dict else 100.0
                verb_weights.append((verb, weight))

            if verb_weights:
                verbs, weights = zip(*verb_weights)
                selected_verbs = random.choices(verbs, weights=weights, k=min(4, len(verbs)))
                session['test_questions'] = [v.id for v in selected_verbs]
            else:
                session['test_questions'] = []

    if session['current_question'] >= len(session['test_questions']):
        return redirect(url_for('test_complete'))

    question_id = session['test_questions'][session['current_question']]

    if test_type == 'vocabulary':
        question = Word.query.get(question_id)
    else:
        question = Verb.query.get(question_id)

    return render_template('real_test.html',
                         question=question,
                         test_type=test_type,
                         question_num=session['current_question'] + 1,
                         total=len(session['test_questions']))

@app.route('/submit-real-answer', methods=['POST'])
def submit_real_answer():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    test_type = session.get('test_type')
    question_id = session['test_questions'][session['current_question']]

    if test_type == 'vocabulary':
        user_answer = request.form.get('answer', '').strip()
        word = Word.query.get(question_id)
        # Real test is English→German, so check German answer with article
        correct_answer = word.german
        correct_with_article = word.article + ' ' + word.german

        # Normalize for umlaut substitutions (ä→ae, ö→oe, ü→ue, ß→ss)
        user_normalized = normalize_umlauts(user_answer.lower())
        correct_normalized = normalize_umlauts(correct_answer.lower())
        correct_with_article_normalized = normalize_umlauts(correct_with_article.lower())

        # Accept with or without article
        is_correct = (user_normalized == correct_normalized or
                     user_normalized == correct_with_article_normalized)

        session['test_answers'].append({
            'word_id': word.id,
            'user_answer': user_answer,
            'correct_answer': correct_with_article,
            'is_correct': is_correct,
            'question': word.english
        })
    else:
        # Verb test - check all 6 conjugations
        verb = Verb.query.get(question_id)
        conjugations = ['ich', 'du', 'er_sie_es', 'wir', 'ihr', 'sie_Sie']
        correct_count = 0
        all_answers = []

        for conj in conjugations:
            user_answer = request.form.get(conj, '').strip()
            correct_answer = getattr(verb, conj)

            # Normalize for umlaut substitutions
            user_normalized = normalize_umlauts(user_answer.lower())
            correct_normalized = normalize_umlauts(correct_answer.lower())

            is_correct = user_normalized == correct_normalized
            if is_correct:
                correct_count += 1

            all_answers.append(f"{conj}: {user_answer}")

            # Store individual conjugation result
            session['test_answers'].append({
                'verb_id': verb.id,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'question': f"{verb.english} ({conj})"
            })

    session['current_question'] += 1

    return jsonify({
        'has_more': session['current_question'] < len(session['test_questions'])
    })

@app.route('/test-complete')
def test_complete():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    is_mock = session.get('is_mock', True)

    if is_mock:
        # Mock test - we already tracked score, now save it
        score = session.get('test_score', 0)
        total = len(session.get('test_questions', []))

        if total > 0:
            percentage = (score / total) * 100

            # Save mock test result
            test_result = TestResult(
                user_id=session['user_id'],
                test_type=session.get('test_type'),
                is_mock=True,
                score=score,
                total=total,
                percentage=percentage
            )
            db.session.add(test_result)
            db.session.commit()
    else:
        # Real test - calculate score and save
        answers = session.get('test_answers', [])
        score = sum(1 for a in answers if a['is_correct'])
        total = len(answers)
        test_type = session.get('test_type')

        if total > 0:
            percentage = (score / total) * 100

            # Save test result
            test_result = TestResult(
                user_id=session['user_id'],
                test_type=session.get('test_type'),
                is_mock=False,
                score=score,
                total=total,
                percentage=percentage
            )
            db.session.add(test_result)
            db.session.commit()

            # Save individual answers
            for answer in answers:
                test_answer = TestAnswer(
                    test_id=test_result.id,
                    word_id=answer.get('word_id'),
                    verb_id=answer.get('verb_id'),
                    user_answer=answer['user_answer'],
                    correct_answer=answer['correct_answer'],
                    is_correct=answer['is_correct']
                )
                db.session.add(test_answer)

            # Update progress for words/verbs
            for answer in answers:
                if 'word_id' in answer and answer['word_id']:
                    progress = WordProgress.query.filter_by(
                        user_id=session['user_id'],
                        word_id=answer['word_id']
                    ).first()
                    if not progress:
                        progress = WordProgress(
                            user_id=session['user_id'],
                            word_id=answer['word_id'],
                            times_seen=0,
                            times_correct=0,
                            times_incorrect=0
                        )
                        db.session.add(progress)
                    progress.times_seen += 1
                    if answer['is_correct']:
                        progress.times_correct += 1
                        # Decrease priority score when correct
                        current_score = progress.priority_score if progress.priority_score is not None else 100.0
                        progress.priority_score = max(1.0, current_score * 0.7)
                    else:
                        progress.times_incorrect += 1
                        # Increase priority score when incorrect
                        current_score = progress.priority_score if progress.priority_score is not None else 100.0
                        progress.priority_score = min(200.0, current_score * 1.5)
                    progress.last_seen = datetime.utcnow()

                elif 'verb_id' in answer and answer['verb_id']:
                    progress = VerbProgress.query.filter_by(
                        user_id=session['user_id'],
                        verb_id=answer['verb_id']
                    ).first()
                    if not progress:
                        progress = VerbProgress(
                            user_id=session['user_id'],
                            verb_id=answer['verb_id'],
                            times_seen=0,
                            times_correct=0,
                            times_incorrect=0
                        )
                        db.session.add(progress)
                    progress.times_seen += 1
                    if answer['is_correct']:
                        progress.times_correct += 1
                        # Decrease priority score when correct
                        current_score = progress.priority_score if progress.priority_score is not None else 100.0
                        progress.priority_score = max(1.0, current_score * 0.7)
                    else:
                        progress.times_incorrect += 1
                        # Increase priority score when incorrect
                        current_score = progress.priority_score if progress.priority_score is not None else 100.0
                        progress.priority_score = min(200.0, current_score * 1.5)
                    progress.last_seen = datetime.utcnow()

            db.session.commit()

    # Store answers and test type before clearing session
    test_answers = session.get('test_answers', []) if not is_mock else []
    stored_test_type = session.get('test_type', 'vocabulary')

    # Clear test session
    session.pop('test_questions', None)
    session.pop('test_type', None)
    session.pop('is_mock', None)
    session.pop('current_question', None)
    session.pop('test_score', None)
    session.pop('test_answers', None)

    percentage = (score / total * 100) if total > 0 else 0
    grade = 'A' if percentage >= 90 else 'B' if percentage >= 80 else 'C' if percentage >= 70 else 'D' if percentage >= 60 else 'F'

    # Get face and snarky comment based on performance
    face_file, face_comment = get_face_and_comment(percentage)

    return render_template('test_complete.html',
                         score=score,
                         total=total,
                         percentage=percentage,
                         grade=grade,
                         is_mock=is_mock,
                         test_answers=test_answers,
                         test_type=stored_test_type,
                         face_file=face_file,
                         face_comment=face_comment)

@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/import-words', methods=['GET', 'POST'])
@admin_required
def admin_import_words():
    if request.method == 'POST':
        csv_data = request.form.get('csv_data', '')
        if not csv_data.strip():
            flash('Please provide CSV data.')
            return redirect(url_for('admin_import_words'))

        # Parse CSV data
        csv_reader = csv.reader(io.StringIO(csv_data))
        imported_count = 0
        skipped_count = 0
        errors = []

        for line_num, row in enumerate(csv_reader, 1):
            if not row or len(row) < 3:
                errors.append(f"Line {line_num}: Invalid format (need at least article, german, english)")
                continue

            article = row[0].strip()
            german = row[1].strip()
            english = row[2].strip()
            level = row[3].strip() if len(row) > 3 else 'A1'

            # Validate level
            if level not in ['A1', 'A2', 'B1', 'B2', 'C1']:
                errors.append(f"Line {line_num}: Invalid level '{level}' (must be A1, A2, B1, B2, or C1)")
                continue

            # Check for duplicates (same german word and article)
            existing = Word.query.filter_by(german=german, article=article).first()
            if existing:
                skipped_count += 1
                continue

            # Add new word
            word = Word(
                article=article,
                german=german,
                english=english,
                level=level
            )
            db.session.add(word)
            imported_count += 1

        db.session.commit()

        flash(f'Successfully imported {imported_count} words. Skipped {skipped_count} duplicates.')
        if errors:
            for error in errors[:5]:  # Show first 5 errors
                flash(error, 'warning')

        return redirect(url_for('admin_import_words'))

    return render_template('admin_import_words.html')

@app.route('/admin/import-verbs', methods=['GET', 'POST'])
@admin_required
def admin_import_verbs():
    if request.method == 'POST':
        csv_data = request.form.get('csv_data', '')
        if not csv_data.strip():
            flash('Please provide CSV data.')
            return redirect(url_for('admin_import_verbs'))

        # Parse CSV data
        csv_reader = csv.reader(io.StringIO(csv_data))
        imported_count = 0
        skipped_count = 0
        errors = []

        for line_num, row in enumerate(csv_reader, 1):
            if not row or len(row) < 8:
                errors.append(f"Line {line_num}: Invalid format (need infinitive, english, ich, du, er_sie_es, wir, ihr, sie_Sie)")
                continue

            infinitive = row[0].strip()
            english = row[1].strip()
            ich = row[2].strip()
            du = row[3].strip()
            er_sie_es = row[4].strip()
            wir = row[5].strip()
            ihr = row[6].strip()
            sie_Sie = row[7].strip()
            level = row[8].strip() if len(row) > 8 else 'A1'

            # Validate level
            if level not in ['A1', 'A2', 'B1', 'B2', 'C1']:
                errors.append(f"Line {line_num}: Invalid level '{level}' (must be A1, A2, B1, B2, or C1)")
                continue

            # Check for duplicates (same infinitive)
            existing = Verb.query.filter_by(infinitive=infinitive).first()
            if existing:
                skipped_count += 1
                continue

            # Add new verb
            verb = Verb(
                infinitive=infinitive,
                english=english,
                ich=ich,
                du=du,
                er_sie_es=er_sie_es,
                wir=wir,
                ihr=ihr,
                sie_Sie=sie_Sie,
                level=level
            )
            db.session.add(verb)
            imported_count += 1

        db.session.commit()

        flash(f'Successfully imported {imported_count} verbs. Skipped {skipped_count} duplicates.')
        if errors:
            for error in errors[:5]:  # Show first 5 errors
                flash(error, 'warning')

        return redirect(url_for('admin_import_verbs'))

    return render_template('admin_import_verbs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
