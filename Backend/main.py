from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Application where everything will be work in pipeline")

origions = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origions,
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get('/')
def welcome():
    return{
        "status" : 200,
        "message" : "Welcome to the automation og HR-Onboarding"
    }