from google import genai
import os
from google.genai._interactions import _response
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

class MCQ(BaseModel):
    question: str = Field(description="Question for the MCQ")
    correct_option: str = Field(description="Correct Option for the question")
    wrong_option_1: str = Field(description="Firt out of four three wrong for the MCQ")
    wrong_option_2: str = Field(description="Second out of three wrong options for the MCQ")
    wrong_option_3: str = Field(description="Third out of three wrong options for the MCQ")
class MCQSet(BaseModel):
    mcqs: List[MCQ]
class WordMCQSet(BaseModel):
    words_mcqs: dict[str, MCQSet] = Field(description="Word and its Set")

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_KEY)
def get_word_details(word_details, context):
    import re
    prompt = f"Please return detailed information about the word: {word_details}. "
    if context:
        prompt += f"The word was used in this context: {context}"
    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": Word.model_json_schema(),
        },
    )
    if not response or not response.text:
        return
    
    # Clean response: remove markdown code blocks
    response_text = response.text
    response_text = re.sub(r'```(?:json)?\s*', '', response_text).strip()
    
    word_details = Word.model_validate_json(response_text)
    word_details = word_details.model_dump()
    return word_details

def generate_mcq(words, contexts: list = []):
    prompt = f"""You are given a list of words. Generate exactly 4 fill-in-the-blank MCQs for each word that test whether the user truly knows what the word means and how it is used.

            Each question is a sentence with a blank (_______) where the target word fits. Each question has 4 options: one correct, three wrong.

            Requirements:
            - The blank must fit the target word naturally and precisely.
            - The wrong options must be genuinely difficult to eliminate. A user who does not know the word's meaning should not be able to guess the answer.

            Words: {words}"""
    if contexts:
        prompt += f"\nContext {contexts}"

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": WordMCQSet.model_json_schema(),
        },
    )
    if not response or not response.text:
        return
    mcq_set = WordMCQSet.model_validate_json(response.text)
    mcq_set = mcq_set.model_dump()
    return mcq_set

words = ["younger", "vulnerable", "years", "father", "advice", "turning", "mind", "criticizing", "remember", "people", "world", "advantages", "communicative", "reserved", "understood", "consequence", "inclined", "reserve", "judgements", "habit", "opened", "curious", "natures", "victim", "veteran", "bores", "abnormal", "quick", "detect", "attach", "quality", "appears", "normal", "person", "college", "unjustly", "accused", "politician", "privy", "secret", "griefs", "wild", "unknown", "men", "confidences", "unsought", "frequently", "feigned", "sleep", "preoccupation", "hostile", "levity", "realized", "unmistakable", "sign", "intimate", "revelation", "quivering", "horizon", "revelations", "young", "terms", "express", "plagiaristic", "marred", "obvious", "suppressions", "reserving", "infinite", "hope", "afraid", "missing", "forget", "snobbishly", "suggested", "repeat", "sense", "fundamental", "decencies", "parcelled", "unequally", "birth", "boasting", "tolerance", "admission", "limit", "conduct", "founded", "hard", "rock", "wet", "marshes", "point", "care", "East", "autumn", "uniform", "moral", "attention", "forever", "riotous", "excursions", "privileged", "glimpses", "human", "heart", "Gatsby", "man", "name", "book", "exempt", "reaction", "represented", "unaffected", "scorn", "personality", "unbroken", "series", "successful", "gestures", "gorgeous", "heightened", "sensitivity", "promises", "life", "related", "intricate", "machines", "register", "earthquakes", "thousand", "miles", "responsiveness", "flabby", "impressionability", "dignified", "creative", "temperament", "extraordinary", "gift", "romantic", "readiness", "likely", "preyed", "foul", "dust", "floated", "wake", "dreams", "temporarily", "closed", "interest", "abortive", "sorrows", "short-winded", "elations"]

part1 = words[0:30]
part2 = words[30:60]
part3 = words[60:90]
part4 = words[90:120]
part5 = words[120:]

import json

parts = [part1, part2, part3, part4, part5]

for i, part in enumerate(parts, start=1):
    result = generate_mcq(part)
    with open(f"mcq_json{i}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
