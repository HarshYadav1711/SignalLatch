# SignalLatch Backend

Local Django backend scaffold for the SignalLatch take-home assignment.

## Stack

- Django
- Django REST Framework
- SQLite

## Project Structure

- `SignalLatch/` - project config (`settings.py`, root `urls.py`)
- `keywords/` - keywords module
- `content/` - content module
- `flags/` - flags module
- `services/` - service-layer module
- `tests/` - project-level tests module

## Setup (Local)

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install django djangorestframework`
3. Run migrations:
   - `python manage.py migrate`
4. Start the server:
   - `python manage.py runserver`

## API Routes (Scaffold)

- `/api/keywords/health/`
- `/api/content/health/`
- `/api/flags/health/`
- `/api/services/health/`

## Mock Dataset

The project uses a local mock dataset file for content import, not a public API:

- `content/data/mock_content.json`
