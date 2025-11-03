# Project Requirements - Learn German App

## Project Overview

A simple, interactive web application for learning German vocabulary and verb conjugations, designed for family use on a Raspberry Pi running 24/7 on a local network.

## Core Requirements

### 1. User Management

**Users**
- Three pre-configured users: sam, sheryl, chris
- Simple authentication: password = username
- No registration system needed
- Individual progress tracking per user

**Security Considerations**
- Local network only (no public internet exposure)
- Simple authentication sufficient
- No password hashing required
- No HTTPS required

### 2. Vocabulary Learning

**Content**
- 231 German nouns
- Each noun has:
  - German word
  - English translation
  - Article (der, die, das)
- Article distribution:
  - der: 83 nouns (masculine)
  - die: 80 nouns (feminine)
  - das: 68 nouns (neuter)

**Categories Covered**
- People & Family (Vater, Mutter, Bruder, Schwester, etc.)
- House & Home (Küche, Schlafzimmer, Tür, Fenster, etc.)
- Food & Drink (Brot, Käse, Milch, Obst, etc.)
- Transportation (Zug, Bus, Flugzeug, Fahrrad, etc.)
- Nature (Baum, Blume, Berg, Fluss, etc.)
- Time (Tag, Woche, Monat, Stunde, etc.)
- Body parts (Kopf, Auge, Hand, Fuß, etc.)
- Clothing (Hemd, Hose, Jacke, Schuh, etc.)
- School & Work (Schule, Büro, Computer, etc.)
- Animals (Hund, Katze, Pferd, etc.)
- Abstract concepts (Liebe, Angst, Wahrheit, etc.)

**Learning Flow**
1. User clicks "Learn Vocabulary"
2. System shows one German word with article
3. User clicks to reveal English translation
4. User marks answer as correct or incorrect
5. System updates progress tracking
6. Next word is selected using smart algorithm

**Smart Selection Algorithm**
- Priority 1: Show unseen words first
- Priority 2: Show words with more incorrect than correct answers
- Priority 3: Random selection from all words

### 3. Verb Conjugation Practice

**Content**
- 78 German verbs
- Each verb has:
  - Infinitive form
  - English translation
  - Present tense conjugations for all pronouns:
    - ich (I)
    - du (you, informal singular)
    - er/sie/es (he/she/it)
    - wir (we)
    - ihr (you, informal plural)
    - sie/Sie (they/you formal)

**Verb Categories**
- Common verbs (sein, haben, werden, etc.)
- Modal verbs (können, müssen, wollen, sollen, dürfen, mögen)
- Action verbs (essen, trinken, schlafen, lesen, schreiben, etc.)
- Movement verbs (gehen, kommen, laufen, fahren, fliegen, etc.)
- Communication verbs (sprechen, sagen, fragen, antworten, etc.)
- Mental/Emotional verbs (denken, lieben, fühlen, glauben, etc.)

**Learning Flow**
1. User clicks "Learn Verbs"
2. System shows random verb with full conjugation table
3. User studies the conjugations
4. "Now You Do It" section appears
5. User fills in all conjugations from memory
6. System checks answers and shows score
7. Progress is tracked

### 4. Mock Tests (Practice Mode)

**Test Configuration**
- 10 random questions per test
- Two test types: vocabulary or verb
- Two directions:
  - German ’ English (show German, answer in English)
  - English ’ German (show English, answer in German)

**Flow**
1. User selects test type and direction on dashboard
2. Questions appear one at a time
3. User types answer and submits
4. Instant feedback:  Correct or  Incorrect with correct answer
5. User clicks "Next Question" or presses Enter
6. After 10 questions, test is complete
7. Results saved to progress

**Answer Validation**
- Case insensitive
- For German ’ English: Accepts "bank" or "the bank"
- For English ’ German: Accepts "Bank" or "die Bank"
- Flexible matching to avoid frustration

### 5. Real Tests (Graded Mode)

**Test Configuration**
- 20 random questions
- Two test types: vocabulary or verb
- Direction: Always English ’ German
- No instant feedback during test

**Flow**
1. User selects test type on dashboard
2. Questions appear one at a time
3. User types answers for all 20 questions
4. No feedback shown during test
5. At the end, system shows:
   - Total score
   - Percentage
   - Letter grade (A-F)
   - List of all questions with user's answers and correct answers

**Grading Scale**
- A: 90-100%
- B: 80-89%
- C: 70-79%
- D: 60-69%
- F: Below 60%

### 6. Progress Tracking

**User Progress Statistics**
- Total time spent learning (in minutes)
- Words learned (unique words seen)
- Verbs learned (unique verbs seen)
- Visual progress bars showing completion percentage

**Test History**
- List of all tests taken (mock and real)
- For each test:
  - Date and time
  - Test type (vocabulary or verb)
  - Mock or real test
  - Score (X out of Y)
  - Percentage
  - Letter grade (for real tests)

**Trending Graphs**
- Chart.js line graph showing test scores over time
- Visual representation of learning progress

**Activity Logs**
- Start time of learning session
- End time of learning session
- Duration in minutes
- Automatic session tracking

### 7. Activity Tracking

**Automatic Time Tracking**
- Starts when user logs in
- Updates on every page request
- Tracks time spent in learning activities
- 5-minute inactivity timeout:
  - If no activity for 5 minutes, session ends
  - Next activity starts new session
  - Previous session's time is calculated and saved

**Session Management**
- Each activity log records:
  - User
  - Start time
  - End time
  - Duration (calculated from start to end)
- Total time is aggregated in user_progress table
- Displayed on progress page

### 8. User Interface Design

**Visual Design**
- Modern, clean interface
- Dark blue gradient background
  - `linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)`
- White card containers for content
- Black text (no playful colors)
- JetBrains Mono font for modern look
- Bootstrap 5 for responsive layout

**Button Design**
- Solid colors (no gradients on buttons)
- Primary buttons: #0066cc (blue)
- Warning buttons: #ff9800 (orange)
- Danger buttons: #f44336 (red)
- Success buttons: #4caf50 (green)

**Navigation**
- Top navigation bar with:
  - App title: "Learn German"
  - Current user name
  - Logout button
- Dashboard with large clickable cards for each section

**Interactivity**
- Rewarding button click experience
- Minimal reading, maximum interaction
- Hover effects on cards
- Focus on clicking and progressing through content

### 9. Database Requirements

**Technology**
- SQLite database
- Flask-SQLAlchemy ORM
- Database file: `instance/learnGerman.db`

**Tables**

1. **user**
   - id (primary key)
   - username (unique)
   - password

2. **word**
   - id (primary key)
   - german (German word)
   - english (English translation)
   - article (der/die/das)

3. **verb**
   - id (primary key)
   - infinitive (German infinitive)
   - english (English translation)
   - ich, du, er_sie_es, wir, ihr, sie_Sie (conjugations)

4. **user_progress**
   - id (primary key)
   - user_id (foreign key)
   - total_time_minutes
   - words_learned
   - verbs_learned

5. **word_progress**
   - id (primary key)
   - user_id (foreign key)
   - word_id (foreign key)
   - times_seen
   - times_correct
   - times_incorrect
   - last_seen (timestamp)

6. **verb_progress**
   - id (primary key)
   - user_id (foreign key)
   - verb_id (foreign key)
   - times_seen
   - times_correct
   - times_incorrect
   - last_seen (timestamp)

7. **test_result**
   - id (primary key)
   - user_id (foreign key)
   - test_type (vocabulary or verb)
   - is_mock (boolean)
   - score (integer)
   - total (integer)
   - percentage (float)
   - date (timestamp)

8. **test_answer**
   - id (primary key)
   - test_result_id (foreign key)
   - word_id (foreign key, nullable)
   - verb_id (foreign key, nullable)
   - user_answer (text)
   - is_correct (boolean)

9. **activity_log**
   - id (primary key)
   - user_id (foreign key)
   - start_time (timestamp)
   - end_time (timestamp)
   - duration_minutes (integer)

### 10. Technical Stack

**Backend**
- Python 3.13+
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- SQLite

**Frontend**
- Bootstrap 5 (CSS framework)
- Chart.js (data visualization)
- Vanilla JavaScript (AJAX for tests)
- Jinja2 templates

**Hosting**
- Raspberry Pi
- Local network only
- Port 8000 (avoid macOS AirPlay port 5000)

**Fonts**
- JetBrains Mono (monospace, modern)
- Loaded from Google Fonts CDN

### 11. Deployment Requirements

**Raspberry Pi Setup**
- Python 3.13+ installed
- Virtual environment for dependencies
- Database initialized with vocabulary
- Flask app runs on boot (optional)

**Network Access**
- Accessible from any device on local network
- IP address: `http://[pi-ip]:8000`
- No external internet exposure

**Performance**
- Must handle 3 concurrent users
- Fast page loads (< 1 second)
- Responsive on mobile devices

### 12. Functional Requirements Summary

**Must Have**
- [x] User authentication (3 users)
- [x] Vocabulary learning with smart selection
- [x] Verb conjugation practice
- [x] Mock tests with instant feedback
- [x] Real tests with grading
- [x] Progress tracking and statistics
- [x] Activity time tracking
- [x] Modern, clean UI
- [x] Responsive design

**Nice to Have** (Future)
- [ ] Past tense verb conjugations
- [ ] Audio pronunciation
- [ ] Spaced repetition algorithm
- [ ] Adjectives learning
- [ ] Custom vocabulary lists
- [ ] User registration system
- [ ] Achievement badges

### 13. Non-Functional Requirements

**Usability**
- Intuitive navigation
- Clear feedback messages
- Minimal clicks to complete tasks
- Family-friendly interface

**Reliability**
- Database integrity maintained
- Proper error handling
- No data loss on crashes
- Session persistence

**Maintainability**
- Clean, documented code
- Easy to add new words/verbs
- Database backup capability
- Version control (Git)

**Performance**
- Page load < 1 second
- Test submission < 500ms
- Progress updates in real-time
- Efficient database queries

**Compatibility**
- Works on desktop browsers (Chrome, Firefox, Safari)
- Works on mobile browsers (iOS, Android)
- Works on tablets
- No special plugins required

### 14. Constraints

**Technical Constraints**
- Must run on Raspberry Pi hardware
- SQLite database (no external DB server)
- Local network only
- Python/Flask framework
- No cloud dependencies

**Security Constraints**
- Local network trust model
- No sensitive data encryption
- Simple password mechanism
- No regulatory compliance needed

**Resource Constraints**
- Raspberry Pi memory limitations
- Single database file
- No CDN for assets (except fonts)
- Minimal external dependencies

### 15. Success Criteria

**Functional Success**
- All 3 users can log in successfully
- Users can learn all 231 words
- Users can practice all 78 verbs
- Tests work correctly with accurate scoring
- Progress is tracked accurately
- Activity time is recorded properly

**User Experience Success**
- Family members enjoy using the app
- Learning feels rewarding and interactive
- UI is clear and not confusing
- Tests feel fair and helpful
- Progress is motivating

**Technical Success**
- App runs 24/7 without crashes
- Database remains consistent
- Performance is acceptable
- Easy to maintain and update

---

**Document Version**: 1.0
**Last Updated**: 2025-11-03
**Status**: Fully Implemented 
