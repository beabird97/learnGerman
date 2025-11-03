from app import app, db
from models import Word

def cleanup_words():
    with app.app_context():
        # Get all words
        all_words = Word.query.all()
        print(f"Total words in database: {len(all_words)}")

        # Find words without articles (not nouns)
        words_to_delete = []
        nouns_with_articles = []
        nouns_without_articles = []

        for word in all_words:
            # Check if word has an article
            if word.article and word.article.lower() in ['der', 'die', 'das']:
                nouns_with_articles.append(word)
            else:
                # Check if the German word is capitalized (German nouns are always capitalized)
                if word.german and word.german[0].isupper():
                    # It's likely a noun but missing article
                    nouns_without_articles.append(word)
                else:
                    # Not a noun - mark for deletion
                    words_to_delete.append(word)

        print(f"\nNouns with articles: {len(nouns_with_articles)}")
        print(f"Nouns missing articles: {len(nouns_without_articles)}")
        print(f"Non-nouns to delete: {len(words_to_delete)}")

        # Show some examples
        if nouns_without_articles:
            print(f"\nFirst 10 nouns without articles:")
            for word in nouns_without_articles[:10]:
                print(f"  {word.german} = {word.english}")

        # Delete non-nouns
        if words_to_delete:
            print(f"\n\nDeleting {len(words_to_delete)} non-nouns...")
            for word in words_to_delete:
                db.session.delete(word)
            db.session.commit()
            print("✓ Deleted non-nouns")

        # For nouns without articles, try to infer from common patterns
        # This is basic - you might want to manually review these
        print(f"\n\nRemoving {len(nouns_without_articles)} nouns without articles...")
        for word in nouns_without_articles:
            db.session.delete(word)
        db.session.commit()
        print("✓ Deleted nouns without articles")

        final_count = Word.query.count()
        print(f"\n✓ Cleanup complete!")
        print(f"✓ Remaining words (nouns with articles): {final_count}")

        # Show some examples
        sample_nouns = Word.query.limit(10).all()
        print(f"\nSample remaining nouns:")
        for word in sample_nouns:
            print(f"  {word.article} {word.german} = {word.english}")

if __name__ == '__main__':
    cleanup_words()
