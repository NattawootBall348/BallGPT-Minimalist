import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple AI Agent function with memory placeholder
def generate_response(prompt: str) -> str:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
    