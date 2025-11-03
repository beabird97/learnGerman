#!/usr/bin/env python3
"""
Script to create or update admin user
"""
from app import app, db
from models import User, UserProgress

def create_admin():
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            # Update existing admin user
            admin.password = 'admin123'
            admin.is_admin = True
            print("Admin user updated successfully!")
        else:
            # Create new admin user
            admin = User(username='admin', password='admin123', is_admin=True)
            db.session.add(admin)
            db.session.commit()
            
            # Create progress entry for admin
            progress = UserProgress(user_id=admin.id)
            db.session.add(progress)
            print("Admin user created successfully!")
        
        db.session.commit()
        print(f"Username: admin")
        print(f"Password: admin123")

if __name__ == '__main__':
    create_admin()
