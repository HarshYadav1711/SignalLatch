# SignalLatch Backend (Django + DRF)

## Project Overview

This is a local-only backend implementation for the SignalLatch take-home assignment.
It is intentionally simple, deterministic, and scoped to the assignment rules.

Core behavior:
- Create normalized keywords
- Run a scan over keywords x content items
- Generate deterministic scores
- Review flags
- Suppress reviewed-irrelevant flags until content changes

## Why a Mock Dataset

The assignment is implemented without paid services, API keys, or external dependencies.
To keep behavior reproducible and free to run, content can be loaded from:

- `content/data/mock_content.json`

If the database already has `ContentItem` rows, scanning uses database content directly.

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite

## Structure

- `SignalLatch/` - project settings and root URL routing
- `keywords/` - keyword domain model, serializer, API create view
- `content/` - content domain model
- `flags/` - flag domain model, serializers, list/review API views
- `services/` - scan and review business logic
- `tests/` - assignment-focused API and service tests

## Local Setup

1. Create a virtual environment
   - Windows PowerShell: `python -m venv .venv`
2. Activate it
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
3. Install dependencies
   - `pip install -r requirements.txt`

## Run Migrations

- `python manage.py makemigrations`
- `python manage.py migrate`

## Run the Server

- `python manage.py runserver`

## Run Tests

- `python manage.py test`

## API Endpoints

- `POST /keywords/` - create a keyword
- `POST /scan/` - trigger a scan
- `GET /flags/` - list flags
- `PATCH /flags/{id}/` - update review status

`GET /flags/` supports simple filters:
- `status` (pending, relevant, irrelevant)
- `min_score` (decimal)
- `keyword` (case-insensitive contains match on keyword name)

## Sample cURL Requests

Create keyword:

```bash
curl -X POST http://127.0.0.1:8000/keywords/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"django\"}"
```

Trigger scan:

```bash
curl -X POST http://127.0.0.1:8000/scan/ \
  -H "Content-Type: application/json" \
  -d "{}"
```

List flags:

```bash
curl "http://127.0.0.1:8000/flags/?status=pending&min_score=40.00&keyword=djan"
```

Mark flag irrelevant:

```bash
curl -X PATCH http://127.0.0.1:8000/flags/1/ \
  -H "Content-Type: application/json" \
  -d "{\"status\":\"irrelevant\"}"
```

## Scoring Rules

Case-insensitive substring checks only (no NLP/fuzzy ranking):

- exact match in title -> `100`
- partial match in title -> `70`
- match only in body -> `40`
- no match -> no flag generated

## Suppression Behavior

When a flag is marked `irrelevant`, the service stores:
- `reviewed_at`
- `reviewed_content_last_updated` (snapshot from `ContentItem.last_updated`)

On future scans:
- If content `last_updated` is unchanged from that snapshot, the flag stays suppressed.
- If content `last_updated` changes, the flag is allowed to re-surface as `pending`.

## Assumptions and Trade-offs

- Matching is intentionally deterministic and explainable over sophisticated relevance.
- The implementation prioritizes assignment clarity over advanced architecture.
- Content uniqueness uses `(source, title)` to avoid obvious duplicates.
- Flag uniqueness uses `(keyword, content_item)` to avoid duplicate flags per pair.
