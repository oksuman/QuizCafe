import re
import random
from typing import List
from pydantic import BaseModel

from api.status_code import StatusCode
from api.nlp import get_ngrams, ner_tagger
from pdf.Pdf2Json import Pdf2Json


class Quiz(BaseModel):
    quiz_num: int
    topic: str
    sentence: str
    answers: List[str]
    source: str


class QuizListResponse(BaseModel):
    response_code: str
    response_message: str
    quiz_count: int
    quizzes: List[Quiz]


def get_quizzes(files):
    pdf = Pdf2Json(files)
    pdf.pdf_to_data()
    data = pdf.TopicList
    print(data)
    ngrams = get_ngrams(data)
    ngrams = dict(sorted(ngrams.items(), key=lambda x: x[1], reverse=True))
    ngrams = dict(filter(lambda x: x[1] < 10, ngrams.items()))
    print(ngrams)

    quiz_num = 1
    quizzes = []

    for d in data:
        topic = d["topic"]
        if topic.lower() in ["목차", "개요", "topics"] or len(topic) >= 30:
            continue
        source = d["file"]
        source += f"p{d['page'][0]}" if len(d["page"]) == 1 else f"p{d['page'][0]}-{d['page'][-1]}"

        for sent in d["sentences"]:
            has_blank = False
            has_next = True
            sentence = ""
            answers = []
            sibling_num = 0
            idx = -1
            tab = ""
            siblings = []
            while has_next:
                text = sent["text"]
                if text.replace(' ', '') == ''.join(sent["keywords"]).replace(' ', ''):
                    sent["keywords"] = []
                keywords = [k.strip(''.join(re.findall(r"[^가-힣a-zA-Z0-9()\s]", k))).strip() for k in sent["keywords"] if k in text]
                if len(keywords) > 0 and "" not in keywords:
                    has_blank = True
                    if len(keywords) >= 2:
                        keywords = random.sample(keywords, 1)
                    answers += keywords
                    for keyword in keywords:
                        text = text.replace(keyword, "[blank]", 1)
                sentence += tab+text
                if idx == sibling_num-1:
                    sibling_num = len(sent["sentences"])
                    tab += '\t'
                    idx = -1
                if sibling_num == 0:
                    has_next = False
                else:
                    idx += 1
                    if idx == 0:
                        siblings = sent["sentences"]
                        sent = sent["sentences"][idx]
                    else:
                        sent = siblings[idx]
            if has_blank:
                if len(re.sub(r"[^가-힣a-zA-Z0-9\s]", "", sentence.replace('[blank]', '')).split()) >= 5:
                    quizzes.append(Quiz(quiz_num=quiz_num, topic=topic, sentence=sentence, answers=answers, source=source))
                    quiz_num += 1
            else:
                keywords = []
                for words in sorted(ngrams.keys(), key=lambda x: len(x), reverse=True):
                    if ''.join(words) in sentence:
                        sentence = sentence.replace(''.join(words), "[blank]", 1)
                        keywords.append(''.join(words))
                        ngrams.pop(words)
                        break
                    elif ' '.join(words) in sentence:
                        sentence = sentence.replace(' '.join(words), "[blank]", 1)
                        keywords.append(' '.join(words))
                        ngrams.pop(words)
                        break
                if len(keywords) > 0:
                    if len(re.sub(r"[^가-힣a-zA-Z0-9\s]", "", sentence.replace('[blank]', '')).split()) >= 5:
                        quizzes.append(Quiz(quiz_num=quiz_num, topic=topic, sentence=sentence, answers=keywords, source=source))
                        quiz_num += 1
                else:
                    ner = ner_tagger(sentence)
                    keywords = [token[0] for token in ner if token[1] in ['TERM', 'THEORY']]
                    keywords = [k.strip(''.join(re.findall(r"[^가-힣a-zA-Z0-9()\s]", k))).strip() for k in keywords if k in sentence]
                    if len(keywords) >= 2:
                        keywords = random.sample(keywords, 1)
                    for keyword in keywords:
                        print(sentence, keywords)
                        sentence = sentence.replace(keyword, "[blank]", 1)
                    if len(keywords) > 0 and len(re.sub(r"[^가-힣a-zA-Z0-9\s]", "", sentence.replace('[blank]', '')).split()) >= 5:
                        quizzes.append(Quiz(quiz_num=quiz_num, topic=topic, sentence=sentence, answers=keywords, source=source))
                        quiz_num += 1

    return QuizListResponse(
        response_code=StatusCode.C20000.code,
        response_message=StatusCode.C20000.message,
        quiz_count=len(quizzes),
        quizzes=quizzes
    )
