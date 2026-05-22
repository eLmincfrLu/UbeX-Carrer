# UBEx — Verified Education to Career Bridge

Hackathon MVP for connecting **students**, **teachers**, **universities**, and **industry partners** through verified skill profiles and AI-assisted vacancy matching.

## Stack

- **Backend:** Flask + SQLAlchemy + Flask-Login
- **Database:** SQLite (`app/database/database.db`)
- **Frontend:** Jinja2 templates, vanilla JS, Chart.js
- **AI (optional):** Gemini API for syllabus skill extraction

## Project structure

```
ubex/
├── app/
│   ├── static/          # css, js, images
│   ├── templates/       # HTML pages
│   ├── routes/          # Blueprints per role
│   ├── models/          # SQLAlchemy models
│   ├── database/        # connection + SQLite file
│   ├── services/        # auth, analytics, gemini
│   ├── utils/
│   └── main.py
├── requirements.txt
├── run.py
└── .env.example
```

## Quick start

```bash
cd UbeX-Carrer
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
copy .env.example .env
python run.py
```

Open http://127.0.0.1:5000

## Demo accounts

| Role       | Email                         | Password    |
|-----------|-------------------------------|-------------|
| Student   | student@university.edu.az     | student123  |
| Teacher   | teacher@university.edu.az     | teacher123  |
| University| admin@university.edu.az       | uni123      |
| Partner   | hr@partner.ubex.local         | partner123  |

## Pitch demo flow

1. **Student** — Show verified skill matrix → one-click apply on vacancy.
2. **Partner** — Post vacancy → view semantic match scores.
3. **University** — Ecosystem analytics dashboard.
4. Emphasize **Verified Profile** during the demo.

## Environment

- `FLASK_SECRET_KEY` — session secret
- `GEMINI_API_KEY` — optional; without it, heuristic skill extraction is used

## Reseed database

Delete `app/database/database.db` and restart the app, or run:

```bash
flask --app app.main seed
```
