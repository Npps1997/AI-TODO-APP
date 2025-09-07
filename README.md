# AI To-Do App (Streamlit + FastAPI + SQLite + Gemini)

## 1) Prereqs
- Python 3.9+
- A Google Gemini API key: https://ai.google.dev/
- Set env var `GOOGLE_API_KEY`

On Windows (PowerShell):
```
$env:GOOGLE_API_KEY="YOUR_KEY_HERE"
```

On macOS/Linux (bash):
```
export GOOGLE_API_KEY="YOUR_KEY_HERE"
```

## 2) Install
```
pip install -r requirements.txt
```

## 3) Run
Open **two terminals**

**Terminal A (backend):**
```
cd backend
uvicorn main:app --reload
```

**Terminal B (frontend):**
```
cd frontend
streamlit run app.py
```

Visit Streamlit URL shown in the terminal (usually http://localhost:8501).

## 4) Endpoints (dev)
- GET  /tasks
- POST /tasks            { "description": "text" }
- PUT  /tasks/{id}       { "description": "optional", "status": "pending|in-progress|done" }
- DELETE /tasks/{id}
- POST /ai/generate-tasks    { "topic": "..." }
- POST /ai/summarize-feedback{ "text": "..." }

## 5) Notes
- DB is SQLite file `tasks.db` created in `backend/` folder.
- Change model name in `backend/main.py` if you want a different Gemini variant.
