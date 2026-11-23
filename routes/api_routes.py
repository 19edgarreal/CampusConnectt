
import os
import sqlite3
from flask import Blueprint, render_template
from utils.api import OpenMeteoAPI

api_bp = Blueprint('api', __name__)

DB_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'db',
        'campusconnect.db'
    )
)


@api_bp.route("/api")
def api():
    # Retrieve current weather and save it to the database.
    weather_api = OpenMeteoAPI()
    weather_api.run()

    # Read saved API data.
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, description, category
        FROM api_data
    """)

    api_data = cursor.fetchall()
    conn.close()

    return render_template(
        "api.html",
        api_data=api_data
    )
