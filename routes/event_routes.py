
import os
import sqlite3
from flask import Blueprint, render_template
from utils.event_scraper import EventScraper

event_bp = Blueprint('event', __name__)

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'db', 'campusconnect.db')
)

@event_bp.route("/events")
def events():
    # Scrape external campus events.
    events_url = "https://www.aic.edu/discover-aic/events-calendar/"
    scraper = EventScraper(events_url)
    scraper.run()

    # Connect to the database.
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get internal campus events.
    cursor.execute("SELECT title, location, date FROM events")
    internal_events = cursor.fetchall()

    # Get external campus events.
    cursor.execute("""
        SELECT title, location, date, description
        FROM external_events
    """)
    external_events = cursor.fetchall()

    conn.close()

    return render_template(
        "events.html",
        internal_events=internal_events,
        external_events=external_events
    )