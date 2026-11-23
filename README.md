# CampusConnect

CampusConnect is a campus community platform designed to help students discover and manage university events.

## Features

- Browse campus events.
- Create and manage events.
- Search for events and view event details.
- Access weather information through the Open-Meteo API.
- Retrieve external event information.

## Technologies

- Python 3.11
- Flask
- SQLite
- Requests
- BeautifulSoup4
- Docker

## Project Setup

1. Clone the repository:

   `git clone https://github.com/19edgarreal/CampusConnectt.git`

2. Open the project folder:

   `cd CampusConnectt`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Initialize the database:

   `sqlite3 db/campusconnect.db < db/schema.sql`

5. Start the application:

   `python app.py`

6. Open your browser at:

   `http://localhost:5000`

## Docker

Build the Docker image:

`docker build -t campusconnect .`

Run the container:

`docker run -p 5000:5000 campusconnect`

Then open `http://localhost:5000`.

## Project Purpose

CampusConnect was developed as an academic MVP to demonstrate event management, backend development, database integration, and containerization.