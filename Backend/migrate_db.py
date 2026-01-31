"""
Database Migration Script
Adds users table to existing database
"""

import sqlite3
import os

# Database path
DB_PATH = "realestate_chat.db"

def migrate_database():
    """Add users table and update chat_sessions table."""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            print("✅ Users table already exists")
        else:
            # Create users table
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Created users table")
        
        # Check if user_id column exists in chat_sessions
        cursor.execute("PRAGMA table_info(chat_sessions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_id' not in columns:
            # Add user_id column to chat_sessions
            cursor.execute("""
                ALTER TABLE chat_sessions 
                ADD COLUMN user_id INTEGER
            """)
            print("✅ Added user_id column to chat_sessions")
        else:
            print("✅ user_id column already exists in chat_sessions")
        
        conn.commit()
        print("\n🎉 Database migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
