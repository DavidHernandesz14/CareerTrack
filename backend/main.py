
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from backend.database import (
    get_connection,
    add_application,
    update_application,
    delete_application,
    create_tables
)


# -------------------------
# APPLICATION DATA MODEL
# -------------------------

class ApplicationCreate(BaseModel):
    company: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)

    status: Literal[
        "Saved",
        "Applied",
        "Interview",
        "Offer",
        "Rejected"
    ] = "Saved"

    date_applied: str | None = None
    notes: str | None = Field(default=None, max_length=2000)

    # Remove extra whitespace and reject blank values
    @field_validator("company", "position")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be blank")

        return value

    # Check that the date is valid
    @field_validator("date_applied")
    @classmethod
    def validate_date(cls, value: str | None) -> str | None:
        if value is None:
            return None

        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError(
                "Date must be a valid date in YYYY-MM-DD format"
            )

        if len(value) != 10 or value[4] != "-" or value[7] != "-":
            raise ValueError(
                "Date must use YYYY-MM-DD format"
            )

        return value


# -------------------------
# DATABASE INITIALIZATION
# -------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


# -------------------------
# CREATE FASTAPI APPLICATION
# -------------------------

app = FastAPI(
    title="CareerTrack API",
    lifespan=lifespan
)


# -------------------------
# FRONTEND CONFIGURATION
# -------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount(
    "/frontend",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend"
)


# -------------------------
# HOME ENDPOINT
# -------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to CareerTrack!",
        "status": "Backend is running"
    }


# -------------------------
# HEALTH CHECK ENDPOINT
# -------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# -------------------------
# GET ALL APPLICATIONS
# -------------------------

@app.get("/applications")
def get_applications():
    connection = get_connection()

    try:
        rows = connection.execute(
            "SELECT * FROM applications"
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


# -------------------------
# CREATE NEW APPLICATION
# -------------------------

@app.post("/applications", status_code=201)
def create_application(application: ApplicationCreate):
    add_application(
        company=application.company,
        position=application.position,
        status=application.status,
        date_applied=application.date_applied,
        notes=application.notes
    )

    return {
        "message": "Application created successfully!"
    }


# -------------------------
# UPDATE EXISTING APPLICATION
# -------------------------

@app.put("/applications/{application_id}")
def edit_application(
    application_id: int,
    application: ApplicationCreate
):
    updated = update_application(
        application_id=application_id,
        company=application.company,
        position=application.position,
        status=application.status,
        date_applied=application.date_applied,
        notes=application.notes
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return {
        "message": "Application updated successfully!"
    }


# -------------------------
# DELETE APPLICATION
# -------------------------

@app.delete("/applications/{application_id}")
def remove_application(application_id: int):
    deleted = delete_application(application_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return {
        "message": "Application deleted successfully!"
    }
