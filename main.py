import pickle
import random

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


origins = [
    "http://localhost:3000",
    "https://ddos-gage.vercel.app",
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


pickleFile = './Decision_Tree_model_on_RENN.pkl'
model = joblib.load(pickleFile)

impFeatureSet = [
    "ACK Flag Count",
    "Active Max",
    "Active Min",
    "Active Std",
    "Avg Packet Size",
    "Bwd Header Length",
    "Bwd IAT Max",
    "Bwd IAT Mean",
    "Bwd IAT Min",
    "Bwd IAT Total",
    "Bwd Packet Length Max",
    "Bwd Packet Length Min",
    "Bwd Packet Length Std",
    "Bwd Packets/s",
    "CWE Flag Count",
    "Down/Up Ratio",
    "Flow Bytes/s",
    "Flow Duration",
    "Flow IAT Mean",
    "Flow Packets/s",
    "Fwd Act Data Packets",
    "Fwd Header Length",
    "Fwd IAT Mean",
    "Fwd IAT Min",
    "Fwd IAT Total",
    "Fwd Packet Length Max",
    "Fwd Packet Length Std",
    "Fwd Seg Size Min",
    "Idle Max",
    "Idle Min",
    "Idle Std",
    "Init Bwd Win Bytes",
    "Init Fwd Win Bytes",
    "Packet Length Min",
    "Packet Length Std",
    "Packet Length Variance",
    "Protocol",
    "RST Flag Count",
    "SYN Flag Count",
    "Subflow Bwd Packets",
    "Total Fwd Packets",
    "URG Flag Count"
  ]

def formatString(strValue):
  dotPos = strValue.find('.')
  s = ""
  typeOfString = 1
  if dotPos == -1:
    # int
    typeOfString = 1
  else:
    # float
    typeOfString = 2
  for i  in strValue:
    if(i >= '0' and i <= '9'):
      s+=i
  if typeOfString == 1:
    if s != '':
        return int(s)
    else:
        return 0
  elif typeOfString == 2:
    if s != '':
        return float(s)
    else:
        return 0.0
  return 0


class Data(BaseModel):
    data: list = []
    param : int = 0

@app.get("/")
async def root():
  return {"data" : "السلام عليكم ورحمة الله وبركاته"}

@app.post("/data")
async def sendDataToBE(data: Data):

  name = "Idle Min\r"

  try:
    data.data[0]["Idle Min\r"]
    name = "Idle Min\r"
  except:
    try:
      data.data[0]["Idle Min"]
      name = "Idle Min"
    except:
      name = ""

  P = []

  randomness= 2

  for row in data.data:
    p = []
    for feature in impFeatureSet:
      if(feature == "Idle Min"):
        if name == "":
          p.append(0.0)
        else:
          if(data.param):
            ran = random.randint(0,randomness)
            p.append(formatString(row[name])+ ran)
          else:
            p.append(formatString(row[name]))
      else:
        if(data.param):
          ran = random.randint(0,randomness)
          p.append(formatString(row[feature])+ ran)
        else:
          p.append(formatString(row[feature]))
    
    P.append(p)

  df = pd.DataFrame(P, columns=impFeatureSet)
  res = (model.predict(df))
  resultArray = []
  for i in res:
    resultArray.append(i)
  return resultArray
