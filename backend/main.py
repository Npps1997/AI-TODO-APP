from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv
from .db_utils import get_db

load_dotenv()

from . import models, schemas, crud, database
from .auth import *

# LangChain + Gemini imports 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="AI Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production to your frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not set in environment")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.3,
    )
    return llm


# ----- User Auth Endpoints -----

@app.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = get_user(db, user_in.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user_in.password)
    new_user = models.User(username=user_in.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# ----- Task CRUD endpoints -----

@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_task(db, task_in, user_id=current_user.id)

@app.get("/tasks", response_model=List[schemas.TaskOut])
def read_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_tasks(db, user_id=current_user.id)

@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    task = crud.update_task(db, task_id, task_in, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = crud.delete_task(db, task_id, user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True}


# ----- AI Endpoints with Auth -----

@app.post("/ai/generate-tasks")
def ai_generate_tasks(payload: dict, current_user: models.User = Depends(get_current_user)):
    topic = payload.get("topic", "").strip()
    if not topic:
        raise HTTPException(status_code=400, detail="topic is required")
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that creates actionable tasks."),
        ("human", "Suggest 5 short, actionable tasks for someone working on {topic}. Return them as a numbered list, each under 12 words.")
    ])
    parser = StrOutputParser()
    chain = prompt | llm
    result = chain.invoke({"topic": topic})
    return {"suggestions": result.content}

@app.post("/ai/summarize-feedback")
def ai_summarize_feedback(payload: dict, current_user: models.User = Depends(get_current_user)):
    text = payload.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize the following student feedback in 3 crisp bullet points."),
        ("human", "Focus on actionable insights and sentiment.\n\nFeedback:\n{text}")
    ])
    chain = prompt | llm
    result = chain.invoke({"text": text})
    return {"summary": result.content}
