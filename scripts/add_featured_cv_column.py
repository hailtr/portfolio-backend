import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'portfolio.db')

def migrate():
    print(f"Migrating database at {DB_PATH}...")
    
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(project)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'is_featured_cv' not in columns:
            print("Adding is_featured_cv column to project table...")
            cursor.execute("ALTER TABLE project ADD COLUMN is_featured_cv BOOLEAN DEFAULT 0")
            print("Column added successfully.")
        else:
            print("Column is_featured_cv already exists.")
            
        conn.commit()
        print("Migration completed successfully.")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
