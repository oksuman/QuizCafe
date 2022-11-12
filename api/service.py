from typing import List
from pydantic import BaseModel

from api.status_code import StatusCode
from Pdf2Json import Pdf2Json


class Quiz(BaseModel):
    topic: str
    sentence: str
    answers: List[str]


class QuizListResponse(BaseModel):
    response_code: str
    response_message: str
    quiz_count: int
    quizzes: List[Quiz]


def get_quizzes(files):
    pdf = Pdf2Json(files)
    pdf.pdf_to_json()
    data = pdf.data

    quizzes = []

    for d in data["output1"]:
        topic = d["Theme"]
        for text in d["Texts"]:
            keywords = text["Keyword"]
            if len(keywords) > 0:
                if text["Text"] != keywords[0] and topic != text["Text"]:
                    quizzes.append(Quiz(topic=topic, sentence=text["Text"], answers=keywords))

    return QuizListResponse(
        response_code=StatusCode.C20000.code,
        response_message=StatusCode.C20000.message,
        quiz_count=len(quizzes),
        quizzes=quizzes
    )
