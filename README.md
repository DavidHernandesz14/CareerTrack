
# CareerTrack

CareerTrack is a full-stack internship application tracking system built using Python, FastAPI, SQLite, HTML, CSS, and JavaScript.

The application allows users to organize internship applications, update their progress, and monitor application statistics through an interactive dashboard.

## Features

- Add new internship applications
- View and manage saved applications
- Edit company, position, status, date, and notes
- Delete applications with confirmation
- Search applications by company or position
- Filter applications by status
- Sort applications by company, date, or status
- View application statistics and status charts
- Persistent storage using SQLite
- Automated backend testing with pytest

## Technologies

**Backend**
- Python
- FastAPI
- SQLite
- Pydantic

**Frontend**
- HTML
- CSS
- JavaScript

**Development Tools**
- Git and GitHub
- Visual Studio Code
- pytest

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd CareerTrack
```

Replace `<repository-url>` with the actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Initialize the database

```bash
python -c "from backend.database import create_tables; create_tables()"
```

### 6. Start the application

```bash
python -m uvicorn backend.main:app --reload
```

### 7. Open the dashboard

Visit:

http://127.0.0.1:8000/frontend/

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Homepage response |
| GET | /health | Health check |
| GET | /applications | Retrieve applications |
| POST | /applications | Create application |
| PUT | /applications/{id} | Update application |
| DELETE | /applications/{id} | Delete application |

Interactive API documentation:

http://127.0.0.1:8000/docs

## Running Tests

Run the automated backend tests using:

```bash
python -m pytest -v
```

The test suite covers API requests, database operations,
validation errors, and missing applications.

Tests use temporary databases to keep local application
data separate.

## Future Improvements

- User authentication
- Application deadline reminders
- Document uploads
- Export applications to CSV
- Deployment to a cloud hosting platform

## Project Status

CareerTrack Version 1.0 is under final review.

The application is designed for local, single-user use.

## Author

David Hernandez
Computer Engineering Student
Cal Poly Pomona
