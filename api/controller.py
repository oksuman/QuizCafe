from typing import List
from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from service import QuizListResponse, get_quizzes

router = APIRouter(tags=["quiz"])


@router.post(path="/quiz", response_model=QuizListResponse)
async def upload_pdf(files: List[UploadFile]):
    files = [await file.read() for file in files]
    result = get_quizzes(files)

    return JSONResponse(
        content=result.dict(),
        status_code=200
    )

quiz_router = router
