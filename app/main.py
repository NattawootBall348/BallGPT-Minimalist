from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal, User, ChatHistory
from app.openai_agent import generate_response
import os

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat", response_class=HTMLResponse)
def chat(request: Request, user_input: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == "Ball").first()
    if not user:
        user = User(name="Ball")
        db.add(user)
        db.commit()
        db.refresh(user)

    ai_response = generate_response(user_input)

    chat_history = ChatHistory(user_id=user.id, user_input=user_input, ai_response=ai_response)
    db.add(chat_history)
    db.commit()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user_input": user_input,
        "ai_response": ai_response
    })