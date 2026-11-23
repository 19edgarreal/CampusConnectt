
import sqlite3
import os

DB_PATH = "db/campusconnect.db"

# Remove the existing database so the seed starts with a clean database.
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# Connect to SQLite and create the database.
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create the users table.
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    preferences TEXT
)
""")

# Create the internal campus events table.
c.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
)
""")

# Create the table for events collected from external college websites.
c.execute("""
CREATE TABLE IF NOT EXISTS external_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT,
    location TEXT,
    description TEXT,
    source_url TEXT
)
""")

# Create the table for data retrieved from public APIs.
c.execute("""
CREATE TABLE IF NOT EXISTS api_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    source_url TEXT
)
""")

# Insert sample users.
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Alice", "Aly"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Bob", "art, Bobby"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Charlie", "Chaz"))

# Insert internal campus events.
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)",
          ("Music Night", "Student Center", "2025-04-05"))

c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)",
          ("Hackathon", "Library", "2025-04-01"))

c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)",
          ("Art Exhibition", "Gallery", "2025-04-10"))

# Insert sample external campus events.
c.execute("""
INSERT INTO external_events (title, date, location, description, source_url)
VALUES (?, ?, ?, ?, ?)
""", ("Campus Welcome Event", "2026-09-01", "Student Center",
       "Welcome event for college students.", "https://example.com/events"))

c.execute("""
INSERT INTO external_events (title, date, location, description, source_url)
VALUES (?, ?, ?, ?, ?)
""", ("Student Club Fair", "2026-09-05", "Campus Quad",
       "Explore student clubs and organizations.", "https://example.com/events"))

# Insert sample API data.
c.execute("""
INSERT INTO api_data (title, description, category, source_url)
VALUES (?, ?, ?, ?)
""", ("Campus Weather", "Sunny weather forecast.", "Weather",
       "https://api.open-meteo.com"))

c.execute("""
INSERT INTO api_data (title, description, category, source_url)
VALUES (?, ?, ?, ?)
""", ("Student Resources", "Helpful information for students.", "Education",
       "https://example.com/api"))

# Save changes and close the database connection.
conn.commit()
conn.close()

print("CampusConnect database seeded successfully!")