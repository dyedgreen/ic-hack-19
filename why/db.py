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
    c.execute("""
        CREATE TABLE IF NOT EXISTS apps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uri TEXT NOT NULL,
            user INTEGER,
            name VARCHAR(32) NOT NULL,
            icon TEXT,
            FOREIGN KEY (user) REFERENCES users(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS reasons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app INTEGER,
            reason TEXT NOT NULL,
            FOREIGN KEY (app) REFERENCES apps(id)
        );
    """)
    conn.commit()
