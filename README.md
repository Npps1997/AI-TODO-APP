# AI-Powered To-Do App

An AI-enhanced task management application built with **FastAPI** for the backend API and **Streamlit** for the frontend UI, integrated with Google Gemini AI to generate task suggestions and summarize feedback.

---

## Features

- User registration and JWT-based authentication
- CRUD operations for user-specific tasks
- AI-powered task suggestion generation via Gemini
- AI-powered summarization of feedback or reviews
- SQLite database for persistent storage
- Clean and responsive UI with Streamlit
- Secure API endpoints with OAuth2 password flow

---

## Project Structure
```
AI_TODO_APP/
├── backend/
│ ├── auth.py # Authentication and JWT token generation
│ ├── crud.py # Database CRUD operations for tasks
│ ├── database.py # SQLAlchemy engine and session creation
│ ├── db_utils.py # Dependency for DB session injection
│ ├── main.py # FastAPI app and route definitions
│ ├── models.py # SQLAlchemy ORM models
│ ├── schemas.py # Pydantic models for validation
│ └── pycache/
├── frontend/
│ └── app.py # Streamlit application UI
├── tasks.db # SQLite database file
├── .env # Environment variables (API keys, secrets)
├── requirements.txt # Python dependencies
└── README.md # This file
```

---


## Getting Started

### Prerequisites

- Python 3.9 or higher
- [Git](https://git-scm.com/)
- Google Cloud API Key for Gemini (set in `.env` as `GOOGLE_API_KEY`)

---

### Installation

1. Clone the repository
```
git clone https://github.com/yourusername/ai-todo-app.git
cd ai-todo-app
```

2. Create and activate a virtual environment
```
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Create a `.env` file and add your Google API key
```
GOOGLE_API_KEY=your-google-cloud-api-key
```


---

### Running the Application

**Start the backend server:**
```
uvicorn backend.main:app --reload
```


**Start the frontend app:**
```
streamlit run frontend/app.py
```
Open your browser and navigate to the Streamlit app URL (usually `http://localhost:8501`).

---

## Usage

- Register a new user and log in.
- Add, update, and delete your tasks.
- Use AI suggestions to generate new actionable tasks based on a given topic.
- Paste feedback text and get an AI-generated summary.

---

## API Documentation

The FastAPI backend automatically hosts interactive API docs at:
```
http://localhost:8000/docs
```


Use this to explore and test backend endpoints.

---

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) — Web API framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM for SQLite database
- [Streamlit](https://streamlit.io/) — Frontend framework for web apps
- [Google Gemini API](https://cloud.google.com/ai) — AI-powered language model
- [OAuth2](https://oauth.net/2/) — Authorization framework for authentication

---

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to fork the repo and submit pull requests.

---

## License

This project is licensed under the MIT License.
