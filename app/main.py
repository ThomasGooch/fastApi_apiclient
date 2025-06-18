from fastapi import FastAPI
from app.routes import patient
from dotenv import load_dotenv

app = FastAPI()

default_response = {"message": "FastAPI Patient API is running."}
load_dotenv()
@app.get("/")
def read_root():
    return default_response

app.include_router(patient.router)
