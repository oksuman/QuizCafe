import re
from typing import List
from pydantic import BaseModel

from api.status_code import StatusCode
from api.nlp import get_ngrams
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
    ngrams = get_ngrams(data)
    ngrams = dict(sorted(ngrams.items(), key=lambda x: x[1], reverse=True))

    quizzes = []

    for d in data:
        topic = d["Theme"]
        if topic in ["목차", "개요"]:
            continue
        sents = []
        for text in d["Texts"]:
            if text["Text"].replace(' ', '') == ''.join(text["Keyword"]).replace(' ', '') or topic == text["Text"]:
                continue
            sentence = text["Text"]
            keywords = [k.lstrip(''.join(re.findall(r"[^가-힣a-zA-Z\s]", k))).strip() for k in text["Keyword"]]
            keywords = [k for k in keywords if k not in topic]
            if len(keywords) > 0 and "" not in keywords:
                pass
                for keyword in keywords:
                    sentence = sentence.replace(keyword, "[blank]", 1)
                if sentence not in sents and len(sentence.replace('[blank]', '')) >= 10:
                    quizzes.append(Quiz(topic=topic, sentence=sentence, answers=keywords))
                    sents.append(sentence)
            else:
                keywords = []
                for words in sorted(ngrams.keys(), key=lambda x: len(x), reverse=True):
                    if ''.join(words) in sentence:
                        sentence = sentence.replace(''.join(words), "[blank]", 1)
                        keywords.append(''.join(words))
                    elif ' '.join(words) in sentence:
                        sentence = sentence.replace(' '.join(words), "[blank]", 1)
                        keywords.append(' '.join(words))
                if len(keywords) > 0 and len(sentence.replace('[blank]', '')) >= 10 and sentence not in sents:
                    quizzes.append(Quiz(topic=topic, sentence=sentence, answers=keywords))
                    sents.append(sentence)

    return QuizListResponse(
        response_code=StatusCode.C20000.code,
        response_message=StatusCode.C20000.message,
        quiz_count=len(quizzes),
        quizzes=quizzes
    )
