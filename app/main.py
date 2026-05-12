from fastapi import FastAPI

from app.api.messages import router as messages_router
from app.db.base import Base
from app.db.session import engine
import app.db.models

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(messages_router)


@app.get("/")
def read_root():
    return {"message": "Message Persistence Service is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}