from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://ddos-app.vercel.app",
    "https://ddos-app-shadreza.vercel.app",
    "https://ddos-app-git-main-shadreza.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data(BaseModel):
    data: object

@app.get("/")
async def root():
  return {"data" : "السلام عليكم ورحمة الله وبركاته"}

@app.post("/data")
async def sendDataToBE(data: Data):
  return data