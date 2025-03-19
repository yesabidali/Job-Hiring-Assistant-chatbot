import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def generate_questions(tech_stack, experience):
    """Generates 4 AI-powered interview questions based on the given tech stack and experience level."""
    
    # Define difficulty levels based on experience
    difficulty_mapping = {
        "<1": "beginner",
        "1-3": "intermediate",
        "3-5": "advanced",
        "5+": "expert"
    }
    
    difficulty = difficulty_mapping.get(experience, "intermediate")  # Default to intermediate
    
    prompt = f"Generate 4 distinct {difficulty} theoretical interview questions for a candidate skilled in {tech_stack}."
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Correct Gemini model
        response = model.generate_content(prompt)  # Correct API method
        
        # Extract text response and clean it
        raw_text = response.text.strip()
        
        # Split into lines and filter unwanted prompt-related text
        questions = [line.strip() for line in raw_text.split("\n") if line.strip()]
        
        # Remove any leading numbering from questions
        cleaned_questions = []
        for line in questions:
            if line.lower().startswith("generate") or "theoretical interview" in line:
                continue  # Skip unwanted lines
            if line[0].isdigit() and line[1:3] in ['. ', ') ']:  # Removing numbers like "1. " or "1) "
                line = line[3:].strip()
            cleaned_questions.append(line)
        
        # Ensure we return exactly 4 questions
        return cleaned_questions[:4] if len(cleaned_questions) >= 4 else ["Error: Fewer than 4 questions generated."]
    
    except Exception as e:
        return [f"Error generating questions: {str(e)}"]