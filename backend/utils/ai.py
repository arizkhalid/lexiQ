from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv(override=True)

class WordForms(BaseModel):
    plural: Optional[str] = Field(description="Plural form, null if not applicable")
    past: Optional[str] = Field(description="Past tense form, null if not applicable")
    comparative: Optional[str] = Field(description="Comparative form, null if not applicable")


class Word(BaseModel):
    word: str = Field(description="The word itself")
    part_of_speech: str = Field(description="The grammatical part of speech")
    definition: str = Field(description="Definition of the word")
    synonyms: Optional[List[str]] = Field(description="Synonyms of the word, return null if none exist")
    antonyms: Optional[List[str]] = Field(description="Antonyms of the word, return null if none exist")
    usage: Optional[str] = Field(description="Usage in a sentence, return null if not applicable")
    examples: Optional[List[str]] = Field(description="Example sentences, return null if none")
    word_register: Optional[str] = Field(description="formal, informal, or slang — return null if unclear")
    connotation: Optional[str] = Field(description="positive, negative, or neutral — return null if unclear")
    collocations: Optional[List[str]] = Field(description="Common collocations, return null if none")
    word_forms: Optional[WordForms] = Field(description="Morphological forms, return null if not applicable")
    derivatives: Optional[List[str]] = Field(description="Derivative words, return null if none")
    etymology: Optional[str] = Field(description="Etymology of the word, return null if unknown")
    notes: Optional[str] = Field(default=None, description="Additional notes or tips, null if none")

import os
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)
WORD = "collocations"
prompt = f"""
Please return detailed information about the word provided {WORD}
"""
def get_word_details(word, context):
    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Word.model_json_schema(),
        },
    )
    recipe = Word.model_validate_json(response.text)
    recipe = recipe.model_dump()
    print(recipe, type(recipe))
    return recipe
get_word_details("test", "test")

