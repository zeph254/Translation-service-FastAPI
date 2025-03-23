import openai
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from crud import update_translation_task

# Load environment variables
load_dotenv()

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def perform_translation(task_id: int, text: str, languages: list, db: Session):
    translations = {}  # Placeholder for actual translation logic
    for lang in languages:
        try:
            response = openai.ChatCompletion.create(  # ✅ Fixed incorrect method call
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a helpful assistant that translates text into {lang}."},
                    {"role": "user", "content": text}
                ],
                max_tokens=1000
            )
            translated_text = response['choices'][0]['message']['content'].strip()  # ✅ Corrected syntax
            translations[lang] = translated_text
        except Exception as e:
            print(f'Error translating to {lang}: {e}')
            translations[lang] = f"Error: {e}"
    
    # Update the translation task in the database
    update_translation_task(db, task_id, translations)
