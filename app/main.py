from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.main import router

app = FastAPI(title="MustageTestTask")
app.include_router(router)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
