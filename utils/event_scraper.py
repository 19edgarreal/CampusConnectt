
import sqlite3
import requests
import re
import os
from bs4 import BeautifulSoup


class EventScraper:
    def __init__(self, events_url):
        # Save the college events calendar URL.
        self.events_url = events_url

        # Locate the SQLite database.
        self.db_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "db", "campusconnect.db")
        )

    def clean_text(self, text):
        # Remove extra spaces and unwanted characters.
        if not text:
            return ""

        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def scrape_events(self):
        # Send a GET request to the college events page.
        try:
            response = requests.get(
                self.events_url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=20
            )
            response.raise_for_status()

        except requests.RequestException as error:
            print(f"Error accessing events page: {error}")
            return []

        # Parse the HTML using BeautifulSoup.
        soup = BeautifulSoup(response.text, "html.parser")
        events = []

        # Find event articles on the college calendar.
        event_elements = soup.select(
            "article, .tribe-events-calendar-list__event-row"
        )

        for element in event_elements:
            title_element = element.select_one(
                ".tribe-events-calendar-list__event-title, "
                ".tribe-event-title, h2, h3"
            )

            date_element = element.select_one(
                "time, .tribe-event-date-start, "
                ".tribe-events-calendar-list__event-datetime"
            )

            location_element = element.select_one(
                ".tribe-events-venue-details, "
                ".tribe-venue, .tribe-events-calendar-list__event-venue"
            )

            description_element = element.select_one(
                ".tribe-events-calendar-list__event-description, "
                ".tribe-event-description, .entry-content, p"
            )

            # Skip elements without an event title.
            if not title_element:
                continue

            title = self.clean_text(title_element.get_text(" ", strip=True))
            date = self.clean_text(
                date_element.get("datetime") or date_element.get_text(" ", strip=True)
            ) if date_element else ""

            location = self.clean_text(
                location_element.get_text(" ", strip=True)
            ) if location_element else "American International College"

            description = self.clean_text(
                description_element.get_text(" ", strip=True)
            ) if description_element else ""

            if title:
                events.append({
                    "title": title,
                    "date": date,
                    "location": location,
                    "description": description
                })

        return events

    def save_events(self, events):
        # Insert scraped events into the external_events table.
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM external_events")

            for event in events:
                cursor.execute("""
                    INSERT INTO external_events
                    (title, date, location, description, source_url)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    event["title"],
                    event["date"],
                    event["location"],
                    event["description"],
                    self.events_url
                ))

            conn.commit()
            print(f"Successfully saved {len(events)} external events.")

        finally:
            conn.close()

    def run(self):
        # Scrape the college calendar and save the results.
        events = self.scrape_events()

        if events:
            self.save_events(events)
        else:
            print("No external events were found.")

        return events
