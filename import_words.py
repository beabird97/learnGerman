import json
from app import app, db
from models import Word

def extract_article(german_word):
    """Extract article from German word if present"""
    parts = german_word.strip().split(' ', 1)
    if len(parts) == 2 and parts[0].lower() in ['der', 'die', 'das']:
        return parts[0], parts[1]
    return None, german_word

def import_words():
    with app.app_context():
        # Load English-German dictionary
        with open('english_german.json', 'r', encoding='utf-8') as f:
            eng_ger = json.load(f)

        print(f"Loaded {len(eng_ger)} English→German translations")

        # Load German-English dictionary
        with open('german_english.json', 'r', encoding='utf-8') as f:
            ger_eng = json.load(f)

        print(f"Loaded {len(ger_eng)} German→English translations")

        # Get existing words to avoid duplicates
        existing_words = {(w.german.lower(), w.english.lower()) for w in Word.query.all()}
        print(f"Found {len(existing_words)} existing words in database")

        new_words = []
        skipped = 0

        # Process German-English (prioritize this since it may have articles)
        for german, english in ger_eng.items():
            german = german.strip()
            english = english.strip()

            # Skip if too long (likely phrases)
            if len(german) > 50 or len(english) > 50:
                skipped += 1
                continue

            # Skip if contains brackets or special formatting
            if '(' in german or ')' in german or '(' in english or ')' in english:
                skipped += 1
                continue

            # Extract article
            article, german_word = extract_article(german)

            # Check if already exists
            if (german_word.lower(), english.lower()) not in existing_words:
                new_words.append(Word(
                    german=german_word,
                    english=english,
                    article=article
                ))
                existing_words.add((german_word.lower(), english.lower()))

        # Add to database in batches
        if new_words:
            print(f"Adding {len(new_words)} new words to database...")
            print(f"Skipped {skipped} complex phrases")

            batch_size = 100
            for i in range(0, len(new_words), batch_size):
                batch = new_words[i:i+batch_size]
                db.session.bulk_save_objects(batch)
                db.session.commit()
                print(f"  Added batch {i//batch_size + 1}/{(len(new_words) + batch_size - 1)//batch_size}")

            print(f"✓ Successfully added {len(new_words)} words!")
            print(f"✓ Total words in database: {Word.query.count()}")
        else:
            print("No new words to add.")

if __name__ == '__main__':
    import_words()
