import pickle

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()


pickleFile = './Decision_Tree_model_on_RENN.pkl'

pickle_in = open(pickleFile, 'rb')
classifiers = pickle.load(pickle_in)

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


model = joblib.load(pickleFile)
pickleFile = './Decision_Tree_model_on_RENN.pkl'

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

class Data(BaseModel):
    data: object

@app.get("/")
async def root():
  return {"data" : "السلام عليكم ورحمة الله وبركاته"}

@app.post("/data")

async def sendDataToBE(data: Data):

  P = []
  p = []

  for feature in impFeatureSet:
    if(feature == "Idle Min"):
      p.append(0.0)
    else:
      p.append(float(data.data[feature]))
  P.append(p)

  df = pd.DataFrame(P, columns=impFeatureSet)

  res = (model.predict(df))
  return res

# @app.post("/predict")

# async def predictData(data: Data):
#   P = []
#   p = []

#   pickleFiles = ['./Models/Central_Trained_Models/Bi-GRUModel.pkl', './Models/Central_Trained_Models/LSTMModel.pkl', './Models/Central_Trained_Models/GRUModel.pkl', './Models/Central_Trained_Models/Bi-LSTMModel.pkl', ]


#   model1C = joblib.load(pickleFiles[0])
#   model2C = joblib.load(pickleFiles[1])
#   model3C = joblib.load(pickleFiles[2])
#   model4C = joblib.load(pickleFiles[3])



#   for feature in impFeatureSet:
#     if(feature == "Idle Min"):
#       p.append(0.0)
#     else:
#       p.append(float(data.data[feature]))
#   P.append(p)
#   print(P)

#   X = pd.DataFrame(P, columns=impFeatureSet)


#   #Making predictions
#   models = [model1C, model2C, model3C, model4C]

#   preds = [model.predict(X) for model in models]
#   preds=np.array(preds)


#   summed = np.sum(preds, axis=0)

#   # # argmax across classes
#   ensemble_prediction = np.argmax(summed, axis=1)


#   counts = np.bincount(ensemble_prediction)
#   max_count_class = np.argmax(counts)
#   return(max_count_class)

