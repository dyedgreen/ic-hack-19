"""
Database
"""

import sqlite3


conn = sqlite3.connect("./data/why-0.db")

# Initialize database
def init():
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(64) NOT NULL UNIQUE,
            password VARCHAR(64),
            salt VARCHAR(64) NOT NULL
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user INTEGER,
            name VARCHAR(64) NOT NULL,
            token VARCHAR(128) UNIQUE,
            created INTEGER NOT NULL,
            FOREIGN KEY (user) REFERENCES users(id)
        );
    """)
    conn.commit()
