from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends        
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import schemas
import models
import crud
from models import get_db
from database import engine
from sqlalchemy.orm import Session
import json

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/index", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def perform_translation(task_id: int, text: str, languages: list, db: Session):
    translations = {}  # Placeholder for actual translation logic
    for lang in languages:
        translations[lang] = f"Translated '{text}' to {lang}"  # Mock translation

    crud.update_translation_task(db, task_id, translations)

@app.post("/translate", response_model=schemas.TaskResponse)
def translate(request: schemas.TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    print("Received Request Data:", request.dict())  # ✅ Log request for debugging

    # Ensure languages is a list
    languages = request.languages if isinstance(request.languages, list) else [request.languages]

    task = crud.create_translation_task(db, request.text, languages)
    background_tasks.add_task(perform_translation, task.id, request.text, languages, db)

    return {"task_id": task.id}

@app.get("/translate/{task_id}", response_model=schemas.TranslationStatus)
def get_translate(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Translation task not found")

    # Ensure `languages` is deserialized correctly
    languages = task.languages if isinstance(task.languages, list) else json.loads(task.languages)

    return {
        "task_id": task.id,
        "status": task.status,
        "text": task.text,
        "languages": languages,
        "translations": task.translations,
    }

@app.get("/translate/content/{task_id}")
def get_translate_content(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Translation task not found")

    # Ensure `languages` is properly formatted
    languages = task.languages if isinstance(task.languages, list) else json.loads(task.languages)

    return {
        "task_id": task.id,
        "status": task.status,
        "text": task.text,
        "languages": languages,
        "translations": task.translations,
    }


from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico", response_class=FileResponse)
async def favicon():
    return FileResponse("static/favicon.ico")
