from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routes import patient

app = FastAPI()

default_response = {"message": "FastAPI Patient API is running."}

@app.get("/")
def read_root():
    return default_response

app.include_router(patient.router)
