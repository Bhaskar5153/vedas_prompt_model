from fastapi import FastAPI
from pydantic import BaseModel
from app.genai_service.llm_service import answer_question

app = FastAPI(title="ISRO VEDAS prompt engg model")

class QuestionRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(req: QuestionRequest):
    try:
        answer = answer_question(req.question)
        return {"question": req.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}