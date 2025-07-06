import os
from google import genai
from dotenv import load_dotenv
from typing import Dict, Any
from pydantic import BaseModel
import json

load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

class ChallengeSchema(BaseModel):
    title: str
    options: list[str]
    correct_answer_id: int
    explanation: str


def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    print("inside")
    prompt='''You are an expert coding challenge creator. 
    Your task is to generate a coding question with multiple choice answers.
    The question should be appropriate for the specified difficulty level'''+ difficulty+'''.

    For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
    For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

    Return the challenge in the following JSON structure:
    {
        "title": "The entire question in ui friendly format",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_answer_id": 0, // Index of the correct answer (0-3)
        "explanation": "Detailed explanation of why the correct answer is right"
    }

    Make sure the options are plausible but with only one clearly correct answer.
    '''
    try:
        response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt,
                        config={
                            "response_mime_type": "application/json",
                            "response_schema": ChallengeSchema,
                        },
                    )
        print("AI Response:",json.loads(response.text)) # json.loads(response.text)
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generating text: {e}")
        return "Error generating text, please try again later."