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

def generate_mcq(word, context: str = ""):
    context_str = ""
    if context:
        context_str = " and the context of its usage"
    prompt = f"""You are given a word{context_str}. Generate exactly 4 fill-in-the-blank MCQs that test whether the user truly knows what the word means and how it is used.

            Each question is a sentence with a blank (_______) where the target word fits. Each question has 4 options: one correct, three wrong.

            Requirements:
            - The blank must fit the target word naturally and precisely.
            - The wrong options must be genuinely difficult to eliminate. A user who does not know the word's meaning should not be able to guess the answer.

            Word: {word}"""

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": MCQSet.model_json_schema(),
        },
    )
    if not response or not response.text:
        return
    mcq_set = MCQSet.model_validate_json(response.text)
    mcq_set = mcq_set.model_dump()
    return mcq_set
