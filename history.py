import sqlite3
import datetime

DB_NAME = 'plant_disease.db'

def init_db():
    """Initialize the database with the history table"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            date TEXT,
            prediction TEXT,
            confidence REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(filename, prediction, confidence):
    """Add a new analysis entry"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO history (filename, date, prediction, confidence) VALUES (?, ?, ?, ?)',
              (filename, date_str, prediction, confidence))
    conn.commit()
    conn.close()

def get_history():
    """Retrieve all history entries, ordered by newest first"""
    conn = sqlite3.connect(DB_NAME)
    row_factory = sqlite3.Row
    conn.row_factory = row_factory
    c = conn.cursor()
    c.execute('SELECT * FROM history ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    
    # Convert sqlite3.Row objects to dictionaries
    history = []
    for row in rows:
        history.append({
            'id': row['id'],
            'filename': row['filename'],
            'date': row['date'],
            'prediction': row['prediction'],
            'confidence': row['confidence']
        })
    return history

# Initialize on module load
init_db()
