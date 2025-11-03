from app import app, db
from models import User, Word, Verb
from werkzeug.security import generate_password_hash
import sqlite3

def update_database():
    """Update database schema and add admin user"""

    with app.app_context():
        # Get database path
        db_path = 'instance/learnGerman.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Add is_admin column to user table if it doesn't exist
        try:
            cursor.execute("ALTER TABLE user ADD COLUMN is_admin BOOLEAN DEFAULT 0")
            print("✓ Added is_admin column to user table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("- is_admin column already exists in user table")
            else:
                raise

        # Add level column to word table if it doesn't exist
        try:
            cursor.execute("ALTER TABLE word ADD COLUMN level VARCHAR(10) DEFAULT 'A1'")
            print("✓ Added level column to word table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("- level column already exists in word table")
            else:
                raise

        # Add level column to verb table if it doesn't exist
        try:
            cursor.execute("ALTER TABLE verb ADD COLUMN level VARCHAR(10) DEFAULT 'A1'")
            print("✓ Added level column to verb table")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print("- level column already exists in verb table")
            else:
                raise

        conn.commit()

        # Update all existing words to A1 level
        cursor.execute("UPDATE word SET level = 'A1' WHERE level IS NULL")
        updated_words = cursor.rowcount
        print(f"✓ Updated {updated_words} words to A1 level")

        # Update all existing verbs to A1 level
        cursor.execute("UPDATE verb SET level = 'A1' WHERE level IS NULL")
        updated_verbs = cursor.rowcount
        print(f"✓ Updated {updated_verbs} verbs to A1 level")

        conn.commit()
        conn.close()

        # Create admin user if doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password=generate_password_hash('admin'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Created admin user (username: admin, password: admin)")
        else:
            # Update existing admin user to ensure is_admin is True
            admin.is_admin = True
            db.session.commit()
            print("- Admin user already exists, ensured is_admin=True")

        print("\n✅ Database migration completed successfully!")

if __name__ == '__main__':
    update_database()
