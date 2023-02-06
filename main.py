import pickle
import time

import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# pickle_in = open('./classifier.pkl', 'rb')
# classifier = pickle.load(pickle_in)

pickle_in = open('./classifiersFour.pkl', 'rb')
classifiers = pickle.load(pickle_in)
knnClassifier = classifiers[1]

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

@app.post("/predict")
async def predictData(data: Data):
  P = [[data.data['height'], data.data['weight'], data.data['shoeSize']]]
  result = []
  for classifier in classifiers: 
    res = classifier.predict(P)
    result.append([str(classifier), res[0], time.time()])
  return result