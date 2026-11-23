
-- CampusConnect database schema

-- Store campus users
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    preferences TEXT
);

-- Store internal campus events
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
);

-- Store events collected from an external college event website
CREATE TABLE IF NOT EXISTS external_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT,
    location TEXT,
    description TEXT,
    source_url TEXT
);

-- Store information retrieved from a public API
CREATE TABLE IF NOT EXISTS api_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    source_url TEXT
);
