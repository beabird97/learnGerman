#!/usr/bin/env python3
"""
Migration script to add priority_score column to WordProgress and VerbProgress tables
"""
import sqlite3

def migrate():
    conn = sqlite3.connect('instance/learnGerman.db')
    cursor = conn.cursor()

    # Check if priority_score column exists in word_progress
    cursor.execute("PRAGMA table_info(word_progress)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'priority_score' not in columns:
        print("Adding priority_score column to word_progress...")
        cursor.execute("ALTER TABLE word_progress ADD COLUMN priority_score REAL DEFAULT 100.0")
        print("✓ Added priority_score to word_progress")
    else:
        print("priority_score already exists in word_progress")

    # Check if priority_score column exists in verb_progress
    cursor.execute("PRAGMA table_info(verb_progress)")
    columns = [row[1] for row in cursor.fetchall()]

    if 'priority_score' not in columns:
        print("Adding priority_score column to verb_progress...")
        cursor.execute("ALTER TABLE verb_progress ADD COLUMN priority_score REAL DEFAULT 100.0")
        print("✓ Added priority_score to verb_progress")
    else:
        print("priority_score already exists in verb_progress")

    conn.commit()
    conn.close()
    print("\nMigration completed successfully!")

if __name__ == '__main__':
    migrate()
