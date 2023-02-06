import pickle
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

app = FastAPI()

# pickle_in = open('./classifier.pkl', 'rb')
# classifier = pickle.load(pickle_in)

pickle_in = open('./classifiersFour.pkl', 'rb')
classifiers = pickle.load(pickle_in)

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
  RandomForestClassifier.predict([[1,1,1]])
  KNeighborsClassifier.predict([[1,1,1]])
  MLPClassifier.predict([[1,1,1]])
  DecisionTreeClassifier.predict([[1,1,1]])
  return data

@app.post("/predict")
async def predictData(data: Data):
  P = [[data.data['height'], data.data['weight'], data.data['shoeSize']]]
  result = []
  for classifier in classifiers: 
    res = classifier.predict(P)
    result.append([str(classifier), res[0], time.time()])
  return result