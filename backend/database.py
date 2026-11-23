
import sqlite3
from pathlib import Path

# Find the CareerTrack project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Choose where our database will be stored
DATABASE_PATH = BASE_DIR / "careertrack.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            status TEXT DEFAULT 'Saved',
            date_applied TEXT,
            notes TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_application(company, position, status="Saved",
                    date_applied=None, notes=None):

    connection = get_connection()

    connection.execute("""
        INSERT INTO applications
        (company, position, status, date_applied, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (company, position, status, date_applied, notes))

    connection.commit()
    connection.close()


def update_application(application_id, company, position,
                       status, date_applied, notes):

    connection = get_connection()

    cursor = connection.execute("""
        UPDATE applications
        SET company = ?,
            position = ?,
            status = ?,
            date_applied = ?,
            notes = ?
        WHERE id = ?
    """, (company, position, status, date_applied,
          notes, application_id))

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated


def delete_application(application_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM applications WHERE id = ?",
        (application_id,)
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted
