from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import quiz_router


def create_app():
    app = FastAPI(title="QuizCafeAPI", version="0.0.1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(quiz_router, prefix="/api/v1")

    return app


app = create_app()
