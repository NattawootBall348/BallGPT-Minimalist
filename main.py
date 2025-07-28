from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Load OpenAI API Key จาก Environment Variable (Railway Variables)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Model สำหรับรับข้อมูล POST
class SumRequest(BaseModel):
    a: int
    b: int

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "BallGPT API is online now!"}

@app.get("/hello")
def say_hello(name: str = "Ball"):
    return {"message": f"Hello {name}, welcome to BallGPT API!"}

@app.post("/sum")
def sum_numbers(data: SumRequest):
    result = data.a + data.b
    return {"result": result}

@app.post("/chat")
def chat_with_gpt(data: ChatRequest):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=data.prompt,
        max_tokens=100
    )
    return {"response": response.choices[0].text.strip()}