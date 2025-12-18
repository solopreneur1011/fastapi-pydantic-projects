from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import requests
from fastapi import Form, HTTPException
from fastapi import UploadFile, File
from typing import Optional

client = OpenAI(
    base_url="http://localhost:11434/v1",  # Ollama local endpoint
    api_key="ollama"  # Dummy key - Ollama doesn't require one
)

try:
    requests.get("http://localhost:11434")
except requests.ConnectionError:
    raise RuntimeError("Ollama is not running. Start it with 'ollama serve'")


class CodeReviewResponse(BaseModel):
    review: str


# initialize app instance
app = FastAPI(
    title="Local AI-Powered Code Review Tool",
    description="An API that reviews code snippets using Ollama (fully local and private)."
)

# get endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Local AI Code Reviewer! Use POST /review to submit code."}


@app.post("/review", response_model=CodeReviewResponse)
async def review_code(
    code: str = Form(...),
    file: Optional[UploadFile] = File(None),
    language: str = Form("python"),
    model: str = Form("gemma2")  # Change to your pulled model
):
    if not code and not file:
        raise HTTPException(status_code=400, detail="Provide either 'code' or 'file'.")

    if file:
        content = await file.read()
        try:
            code = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File must be text/UTF-8 encoded.")

    if not code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty.")

    system_prompt = (
        f"You are an expert {language} code reviewer. "
        "Analyze the code for bugs, performance issues, style problems, security risks, "
        "and suggest concrete improvements. Be thorough but constructive."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": code}
            ],
            max_tokens=1500,
            temperature=0.5   # ??
        )
        review = response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI review failed: {str(e)}")

    return CodeReviewResponse(review=review)

