import os 
import json
from openai import OpenAI
from typing import Dict, Any
from backend.schemas import FillInTheBlankExercise, MultipleChoiceExercise

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_vocabulary_exercise(
    target_word: str,
    difficulty: str = 'Intermediate',
    exercise_type: str = 'fill_in_the_blank',
) -> Dict[str, Any]:
    """
    Generates a structured vocabulary exercise using OpenAI's API.

    Args:
        target_word: The word for the exercise (e.g., 'ubiquitous').
        
    Returns:
        A dictionary containing the structured exercise data.
    """
    if exercise_type == 'fill_in_the_blank':
        target_schema = FillInTheBlankExercise
    else:
        target_schema = MultipleChoiceExercise

    system_prompt = (
        "You are an expert vocabulary exercise generator. "
        "Your only job is to create a single, valid vocabulary exercise "
        "based on the user's request and strictly adhere to the provided JSON schema. "
        "Do not include any text or commentary outside of the JSON object."
    )

    user_prompt = (
        f"Generate a '{exercise_type}' exercise for the word '{target_word}'. "
        f"The difficulty should be '{difficulty}'. "
        "Populate all fields in the JSON schema."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # A great model for structured output
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            # This is the key part: enforcing the JSON output structure
            response_format={"type": "json_object", "schema": target_schema.schema()}
        )

        # The response content is a guaranteed valid JSON string
        json_string = response.choices[0].message.content
        
        # --- 4. Parse the JSON string into a Python dictionary ---
        return json.loads(json_string)

    except Exception as e:
        print(f"An error occurred during OpenAI call: {e}")
        return {}
    
    
    return _json.loads(str(response))