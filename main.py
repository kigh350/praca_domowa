from typing import Dict
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
#import sqlite3
#import os
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/method")
def read_item():
    return {"method": "GET"}

@app.post("/method")
def read_item():
    return {"method": "POST"}

@app.delete("/method")
def read_item():
    return {"method": "DELETE"}

@app.put("/method")
def read_item():
    return {"method": "PUT"}

class im_nazw(BaseModel):
    name: str 
    surename: str = "SURENAME"

patient = im_nazw(
    name="NAME",
    surename="SURENAME"
)

class im_nazw_Resp(BaseModel):
    id: int
    patient: Dict

n=0
lista=[n]
@app.post("/patient", response_model=im_nazw_Resp)
def receive_patient(rq: im_nazw):
    global n
    global wynik
    global lista
    n += 1
    lista[n] = n
    slownik = im_nazw_Resp(id=n, patient=rq.dict())
    wynik = slownik.dict()
    return wynik

@app.get("/patient/{pk}")
def read_item(pk: int):
    if pk not in lista:
        raise HTTPException(status_code=204, detail="Item not found")
    else:
        results = patient
    return results
