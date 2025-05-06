from fastapi import FastAPI
import config
from fastapi.middleware.cors import CORSMiddleware
import endpoints

app = FastAPI()

app.include_router(endpoints.router)

# origins = config.cors_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)