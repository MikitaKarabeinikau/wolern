import os 
import json
from openai import OpenAI
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_vocabulary_exercise(
    target_word: str,
    difficulty: str
) -> Dict[str, Any]:
    """
    Generates a structured vocabulary exercise using OpenAI's API.

    Args:
        target_word: The word for the exercise.
        difficulty: The difficulty level for the exercise.
        
    Returns:
        A dictionary containing the structured exercise data.
    """
    
    # Define the desired JSON structure
    json_schema = {
        "exercise": {
            "word": "string",
            "difficulty": "string (e.g., Beginner, Intermediate, Advanced)",
            "part_of_speech": "string",
            "question": "string",
            "explanation": "string",
            "hints": ["string"]
        },
        "multiple_choice": {
            "options": ["string"],
            "correct_answer": "integer (index of the correct option)"
        }
    }

    system_prompt = f"""
    You are an expert vocabulary exercise generator. 
    Your only job is to create a single, valid vocabulary exercise 
    based on the user's request and strictly adhere to the provided JSON schema.
    
    Return the exercise in the following JSON structure:
    {json.dumps(json_schema, indent=4)}

    Make sure the options are plausible but only one is correct.
    """  
    
    user_prompt = f"""
    Create a vocabulary exercise for the word '{target_word}' with difficulty '{difficulty}'.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Use a valid model name
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        exercise_data = json.loads(content)
        
        # --- Validation ---
        if 'exercise' not in exercise_data or 'multiple_choice' not in exercise_data:
            raise ValueError("Generated JSON is missing 'exercise' or 'multiple_choice' keys.")

        required_fields_exercise = ['word', 'difficulty', 'part_of_speech', 'question', 'explanation', 'hints']
        required_fields_mc = ['options', 'correct_answer']
        
        if all(field in exercise_data['exercise'] for field in required_fields_exercise) and \
           all(field in exercise_data['multiple_choice'] for field in required_fields_mc):
            return exercise_data
        else:
            raise ValueError("Generated exercise does not conform to the required schema.")  
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in AI generator: {e}")
        raise RuntimeError(f"Failed to generate exercise: {e}")
