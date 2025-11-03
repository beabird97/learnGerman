from app import app, db
from models import Word, WordProgress, TestAnswer

def delete_words_after_105():
    with app.app_context():
        # First, check what we have
        total_words = Word.query.count()
        words_to_delete = Word.query.filter(Word.id > 105).count()

        print(f"Total words in database: {total_words}")
        print(f"Words with id > 105: {words_to_delete}")

        # Get word IDs to delete
        word_ids_to_delete = [w.id for w in Word.query.filter(Word.id > 105).all()]

        if not word_ids_to_delete:
            print("\nNo words to delete.")
            return

        print(f"\nDeleting related records first...")

        # Delete WordProgress records first (foreign key constraint)
        progress_count = WordProgress.query.filter(WordProgress.word_id.in_(word_ids_to_delete)).count()
        if progress_count > 0:
            print(f"  Deleting {progress_count} WordProgress records...")
            WordProgress.query.filter(WordProgress.word_id.in_(word_ids_to_delete)).delete(synchronize_session='fetch')
            db.session.commit()
            print(f"  ✓ Deleted {progress_count} WordProgress records")

        # Delete TestAnswer records
        test_answer_count = TestAnswer.query.filter(TestAnswer.word_id.in_(word_ids_to_delete)).count()
        if test_answer_count > 0:
            print(f"  Deleting {test_answer_count} TestAnswer records...")
            TestAnswer.query.filter(TestAnswer.word_id.in_(word_ids_to_delete)).delete(synchronize_session='fetch')
            db.session.commit()
            print(f"  ✓ Deleted {test_answer_count} TestAnswer records")

        # Now delete the words
        print(f"\nDeleting {words_to_delete} words with id > 105...")
        Word.query.filter(Word.id > 105).delete(synchronize_session='fetch')
        db.session.commit()
        print(f"✓ Deleted {words_to_delete} words")

        # Verify
        remaining_words = Word.query.count()
        print(f"\n✓ Cleanup complete!")
        print(f"✓ Remaining words: {remaining_words}")

        # Show sample
        print(f"\nSample remaining words:")
        for word in Word.query.limit(10).all():
            print(f"  ID {word.id}: {word.article} {word.german} = {word.english}")

if __name__ == '__main__':
    delete_words_after_105()
