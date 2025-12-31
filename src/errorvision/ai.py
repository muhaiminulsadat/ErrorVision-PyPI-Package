import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# placeholder: import your Gemini API client
# from gemini import Client


def get_model_response(prompt: str, model: str = "openai/gpt-oss-20b") -> str:

    # Initialize client
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

    # Call the model
    response = client.responses.create(model=model, input=prompt)

    return response.output_text


AI_ENABLED = os.getenv("AI", "true").lower() == "true"
GEMINI_KEY = os.getenv(
    "GROQ_API_KEY"
)


def get_ai_explanation(error_name, code_line, message):
    if not AI_ENABLED or not GEMINI_KEY:
        return None
    prompt = f"""
        You are a Python tutor.

        Explain the following error for a beginner.

        Rules:
        - Max 3 short lines
        - No introductions
        - No emojis
        - No markdown
        - No extra explanations

        Format EXACTLY like this:
        - Reason: <one short sentence>
        - Fix: <one short instruction>
        - Example: 
            <short code line>

        Error type: {error_name}
        Code line: {code_line}
        Message: {message}
        """

    # TODO: call Gemini API with prompt and return explanation
    # response = client.ask(prompt)
    response = get_model_response(prompt)
    return response