import sqlite3
import os
import datetime
import json
from contextlib import contextmanager

DATABASE_PATH = 'data/pet_database.sqlite'

def ensure_database_exists():
    """Ensure database directory and tables exist"""
    os.makedirs('data', exist_ok=True)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            level INTEGER DEFAULT 1,
            experience INTEGER DEFAULT 0,
            last_login TEXT,
            github_username TEXT,
            puzzles_solved INTEGER DEFAULT 0
        )
        ''')
        
        # Create journal entries table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            entry_date TEXT,
            content TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            UNIQUE(user_id, entry_date)
        )
        ''')
        
        # Create github commits table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS github_commits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            commit_date TEXT,
            commit_count INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            UNIQUE(user_id, commit_date)
        )
        ''')
        
        conn.commit()

@contextmanager
def get_connection():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def get_user_profile(user_id):
    """Get user profile from database, create if doesn't exist"""
    ensure_database_exists()
    user_id = str(user_id)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Try to get existing user
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            # Create new user if not found
            cursor.execute(
                "INSERT INTO users (user_id, level, experience) VALUES (?, 1, 0)",
                (user_id,)
            )
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        user_dict = dict(zip(columns, user))
        
        # Add journal days
        cursor.execute(
            "SELECT entry_date, content FROM journal_entries WHERE user_id = ?",
            (user_id,)
        )
        journal_days = {row[0]: row[1] for row in cursor.fetchall()}
        user_dict['journal_days'] = journal_days
        
        # Add github commits
        cursor.execute(
            "SELECT commit_date, commit_count FROM github_commits WHERE user_id = ?",
            (user_id,)
        )
        github_commits = {row[0]: row[1] for row in cursor.fetchall()}
        user_dict['github_commits'] = github_commits
        
        return user_dict

def add_experience(user_id, amount):
    """Add experience points and check for level up"""
    user_id = str(user_id)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Update experience
        cursor.execute(
            "UPDATE users SET experience = experience + ? WHERE user_id = ?",
            (amount, user_id)
        )
        conn.commit()
        
        return check_level_up(user_id, conn)

def check_level_up(user_id, conn=None):
    """Check if user can level up, returns true if leveled up"""
    from config import calculate_level_requirement
    user_id = str(user_id)
    
    should_close = False
    if conn is None:
        conn = sqlite3.connect(DATABASE_PATH)
        should_close = True
    
    try:
        cursor = conn.cursor()
        
        # Get current level and experience
        cursor.execute("SELECT level, experience FROM users WHERE user_id = ?", (user_id,))
        level, experience = cursor.fetchone()
        
        level_req = calculate_level_requirement(level)
        
        if experience >= level_req:
            # Level up
            cursor.execute(
                "UPDATE users SET level = level + 1 WHERE user_id = ?",
                (user_id,)
            )
            conn.commit()
            return True
        return False
    
    finally:
        if should_close:
            conn.close()

def update_login(user_id, today=None):
    """Update user's last login date"""
    user_id = str(user_id)
    if today is None:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET last_login = ? WHERE user_id = ?",
            (today, user_id)
        )
        conn.commit()

def add_journal_entry(user_id, entry, date=None):
    """Add journal entry for user"""
    user_id = str(user_id)
    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO journal_entries (user_id, entry_date, content) VALUES (?, ?, ?)",
                (user_id, date, entry)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Entry for this date already exists
            return False

def update_github_username(user_id, github_username):
    """Update GitHub username for user"""
    user_id = str(user_id)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET github_username = ? WHERE user_id = ?",
            (github_username, user_id)
        )
        conn.commit()

def record_github_commits(user_id, date, commit_count):
    """Record GitHub commits for a specific date"""
    user_id = str(user_id)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO github_commits (user_id, commit_date, commit_count) VALUES (?, ?, ?)",
                (user_id, date, commit_count)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Update existing record
            cursor.execute(
                "UPDATE github_commits SET commit_count = ? WHERE user_id = ? AND commit_date = ?",
                (commit_count, user_id, date)
            )
            conn.commit()
            return True

def increment_puzzles_solved(user_id):
    """Increment puzzles solved counter for user"""
    user_id = str(user_id)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET puzzles_solved = puzzles_solved + 1 WHERE user_id = ?",
            (user_id,)
        )
        conn.commit()

def migrate_from_json():
    """Migrate data from JSON file to SQLite database"""
    json_path = 'data/pet_data.json'
    if not os.path.exists(json_path):
        return
        
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            
        ensure_database_exists()
        
        with get_connection() as conn:
            cursor = conn.cursor()
            
            for user_id, profile in data.items():
                # Insert or update user
                cursor.execute(
                    """
                    INSERT INTO users 
                    (user_id, level, experience, last_login, github_username, puzzles_solved) 
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                    level = excluded.level,
                    experience = excluded.experience,
                    last_login = excluded.last_login,
                    github_username = excluded.github_username,
                    puzzles_solved = excluded.puzzles_solved
                    """,
                    (
                        user_id, 
                        profile.get('level', 1),
                        profile.get('experience', 0),
                        profile.get('last_login'),
                        profile.get('github_username'),
                        profile.get('puzzles_solved', 0)
                    )
                )
                
                # Insert journal entries
                for date, entry in profile.get('journal_days', {}).items():
                    try:
                        cursor.execute(
                            "INSERT INTO journal_entries (user_id, entry_date, content) VALUES (?, ?, ?)",
                            (user_id, date, entry)
                        )
                    except sqlite3.IntegrityError:
                        pass  # Entry already exists
                
                # Insert github commits
                for date, count in profile.get('github_commits', {}).items():
                    try:
                        cursor.execute(
                            "INSERT INTO github_commits (user_id, commit_date, commit_count) VALUES (?, ?, ?)",
                            (user_id, date, count)
                        )
                    except sqlite3.IntegrityError:
                        pass  # Entry already exists
            
            conn.commit()
            
        # Backup the JSON file
        backup_path = f"{json_path}.bak"
        os.rename(json_path, backup_path)
        print(f"Data migrated successfully. Original file backed up to {backup_path}")
        
    except Exception as e:
        print(f"Migration error: {e}")

# Run migration when module is imported
if __name__ == "__main__":
    migrate_from_json()