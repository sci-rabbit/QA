import logging

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.views.answer_view import router as answer_router
from api.views.question_view import router as question_router
from core.database import dispose

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        # logging.FileHandler("/app/logs/bot.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(question_router)
app.include_router(answer_router)


@app.get("/health")
def healthcheck():
    return {"msg": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
