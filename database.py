import sqlite3
from pathlib import Path


DB_PATH = Path("data/attendance.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'attendee'
        )
    """)

    # Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            start_time TEXT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            allowed_radius REAL DEFAULT 100,
            qr_token TEXT UNIQUE NOT NULL
        )
    """)

    # Attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            distance REAL,
            status TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(event_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully!")