# Notes App Backend (Flask) - Ocean Professional

A modern, clean RESTful API for managing notes using Flask and flask-smorest. Responses and docs follow the "Ocean Professional" theme with blue and amber accents.

## Endpoints

- GET `/` — Health check
- GET `/notes` — List notes (`include_archived=true|false`)
- POST `/notes` — Create note
- GET `/notes/{id}` — Get note by id
- PUT `/notes/{id}` — Update note (partial/full)
- DELETE `/notes/{id}` — Delete note
- GET `/notes/search?q={query}` — Search notes

## Run locally

```
cd notes_app_backend
pip install -r requirements.txt
python run.py
```

The service binds to `0.0.0.0:3001` for container readiness. Docs available at `/docs` (Swagger UI).

Optional production run (example):

```
# from notes_app_backend/
gunicorn -w 2 -b 0.0.0.0:3001 'run:create_app()'
```

No environment variables are required. In-memory storage is used for simplicity.
