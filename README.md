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
│   ├── static/          # css, js, images bu fayllar burdadair
│   ├── templates/       # HTML seyfeleri
│   ├── routes/
│   ├── models/          # SQLAlchemy modeli bu qovluqda olacaq
│   ├── database/        # sql lite istifade etmisik
│   ├── services/
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
.venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
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

## CV + AI flow (students)

1. Register as **Student** → redirected to **Upload CV**
2. Upload PDF/TXT → AI extracts skills → **Dashboard** shows skill matrix & chart
3. Profile page can re-analyze or upload a new CV

CV files are stored in `app/uploads/cvs/` (not in git).

## Pitch demo flow

1. **Student** — Upload CV (or use demo account) → verified skill matrix → one-click apply.
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
