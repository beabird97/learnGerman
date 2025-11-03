# TODO List - Learn German App

## Completed Features 

- [x] User authentication system (3 users: sam, sheryl, chris)
- [x] Vocabulary learning module (231 nouns with articles)
- [x] Verb conjugation practice (78 verbs)
- [x] Mock tests with instant feedback
- [x] Real tests with grading (A-F)
- [x] Progress tracking (time, words/verbs learned, test history)
- [x] Activity time tracking with 5-minute inactivity timeout
- [x] Smart learning algorithm (prioritizes unseen/difficult items)
- [x] Flexible answer validation (with/without articles)
- [x] Direction choice for mock tests (German’English or English’German)
- [x] Visual progress bars
- [x] Test result history with trending graphs
- [x] Bootstrap 5 UI with JetBrains Mono font
- [x] Dark blue gradient background
- [x] Enter key support for advancing test questions
- [x] Database cleanup scripts
- [x] Comprehensive vocabulary (231 nouns, 78 verbs)

## Potential Future Enhancements

### High Priority

- [ ] **Past Tense Verb Conjugations**
  - Add past tense (Präteritum) conjugations to verb table
  - Add past tense practice mode
  - Update tests to include past tense questions

- [ ] **Audio Pronunciation**
  - Add German pronunciation audio for words and verbs
  - Use text-to-speech API or pre-recorded audio files
  - Add speaker icon to play pronunciation

- [ ] **Adjectives Learning Module**
  - Add adjective declension tables
  - Practice adjective endings with different articles
  - Add adjectives to vocabulary tests

- [ ] **Spaced Repetition Algorithm**
  - Implement SRS (like Anki) based on last_seen and performance
  - Calculate optimal review intervals
  - Show "due for review" count on dashboard

- [ ] **User Statistics Dashboard**
  - Current streak tracking (days in a row)
  - Weekly/monthly activity heatmap
  - Most difficult words/verbs list
  - Average test scores over time

### Medium Priority

- [ ] **Custom Vocabulary Lists**
  - Allow users to create custom word collections
  - Practice specific categories (food, travel, etc.)
  - Import/export word lists

- [ ] **Sentence Construction Practice**
  - Build sentences using learned words
  - Grammar checking
  - Common phrase patterns

- [ ] **Plural Forms**
  - Add plural forms for nouns
  - Practice singular/plural recognition
  - Add to vocabulary tests

- [ ] **Case System Practice (Nominative, Accusative, Dative, Genitive)**
  - Add article declension tables
  - Practice mode for different cases
  - Sentence-based case exercises

- [ ] **User Management Improvements**
  - User registration page
  - Password hashing (bcrypt)
  - Password reset functionality
  - User profile settings

- [ ] **Test Improvements**
  - Customizable test length (5, 10, 15, 20 questions)
  - Test difficulty levels (beginner, intermediate, advanced)
  - Timed tests with countdown timer
  - Review incorrect answers after test

- [ ] **Mobile Responsive Improvements**
  - Optimize for phone/tablet screens
  - Touch-friendly buttons
  - Mobile navigation menu

### Low Priority / Nice to Have

- [ ] **Dark Mode Toggle**
  - User preference for dark/light theme
  - Save preference in database

- [ ] **Achievement Badges**
  - Milestones (10 words learned, 50 words learned, etc.)
  - Perfect test scores
  - Streak achievements

- [ ] **Leaderboard**
  - Compare scores between family members
  - Most words learned this week
  - Highest test scores

- [ ] **Export Progress**
  - Download progress as PDF report
  - Export vocabulary lists to CSV
  - Print flashcards

- [ ] **Word of the Day**
  - Daily featured word on dashboard
  - Notification/reminder system

- [ ] **Conjugation Games**
  - Matching game (infinitive to conjugation)
  - Fill-in-the-blank stories
  - Timed challenges

- [ ] **Listening Comprehension**
  - Audio questions (hear German, type answer)
  - Dictation exercises

- [ ] **German Keyboard Helper**
  - Virtual keyboard for umlauts (ä, ö, ü, ß)
  - Auto-convert ae’ä, oe’ö, ue’ü, ss’ß

- [ ] **Study Reminders**
  - Email/notification reminders
  - Configurable study schedule

## Technical Improvements

### Code Quality

- [ ] **Add Unit Tests**
  - Test models
  - Test routes
  - Test answer validation logic
  - Test activity tracking

- [ ] **Add Integration Tests**
  - Full user flow tests
  - Database transaction tests

- [ ] **Code Documentation**
  - Add docstrings to all functions
  - Type hints for function parameters
  - Document complex algorithms

- [ ] **Error Handling**
  - Proper error pages (404, 500)
  - User-friendly error messages
  - Logging for debugging

### Performance

- [ ] **Database Optimizations**
  - Add indexes on frequently queried fields
  - Optimize slow queries
  - Consider database migrations tool (Alembic)

- [ ] **Caching**
  - Cache frequently accessed data
  - Session-based caching for test questions

- [ ] **Frontend Optimizations**
  - Minify CSS/JavaScript
  - Compress images
  - Lazy loading for progress charts

### Security (if deploying beyond local network)

- [ ] **Security Hardening**
  - Add CSRF protection
  - Add password hashing (bcrypt)
  - Add HTTPS/SSL
  - Rate limiting for login attempts
  - Input sanitization
  - SQL injection prevention (already using ORM, but verify)

- [ ] **Production Configuration**
  - Disable debug mode
  - Use production WSGI server (Gunicorn)
  - Set up proper logging
  - Environment variables for secrets

### Deployment

- [ ] **Raspberry Pi Setup Script**
  - Auto-install dependencies
  - Configure systemd service for auto-start
  - Setup script for first-time installation

- [ ] **Database Backup**
  - Automated backup script
  - Backup to external storage/cloud

- [ ] **Update Mechanism**
  - Easy way to pull new words/verbs
  - Database migration strategy

## Bugs / Known Issues

- [ ] **Database Lock Errors**
  - Occasionally occurs when database is open elsewhere
  - Need better error handling and user messaging

- [ ] **Session Timeout**
  - No warning before session expires
  - Consider adding session timeout warning

- [ ] **Multiple Flask Instances**
  - Multiple background processes can cause conflicts
  - Add process management

## Documentation Needed

- [x] README.md with setup instructions
- [x] CODE_GUIDE.md with architecture explanation
- [x] TODO.md with future enhancements (this file)
- [x] REQUIREMENTS.md with feature specifications
- [ ] API documentation (if adding API endpoints)
- [ ] User manual / tutorial for family members
- [ ] Troubleshooting guide

## Version History

### v1.0 (Current)
- Initial release with core features
- 231 nouns, 78 verbs
- Vocabulary and verb learning
- Mock and real tests
- Progress tracking
- Activity monitoring

### Future Versions

**v1.1** (Planned)
- Past tense verb support
- Audio pronunciation
- Spaced repetition algorithm

**v1.2** (Planned)
- Adjectives module
- Custom vocabulary lists
- Enhanced statistics

**v2.0** (Future)
- Sentence construction
- Case system practice
- Mobile app version

---

**Note**: This is a living document. Update as features are completed or new ideas emerge.

**Last Updated**: 2025-11-03
