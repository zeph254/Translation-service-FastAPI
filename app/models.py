from sqlalchemy import Column, Integer, String, Boolean ,Text , JSON
from database import SessionLocal
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TranslationTask(Base):
    __tablename__ = "translation_tasks"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    languages = Column(JSON, nullable=False)
    status = Column(String, default = "in_progress")
    translations = Column(JSON , default = {})