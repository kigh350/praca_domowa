from typing import Dict
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel
#import sqlite3
import os
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
    surename: str


class im_nazw_Resp(BaseModel):
    id: int
    patient: Dict
    
class im_nazw_pat(BaseModel):
    Dict    
 
n=0
slownik_id = {}
@app.post("/patient", response_model=im_nazw_Resp)
def receive_patient(rq: im_nazw):
    global slownik_id
    global n
    slownik_id = {n: rq}
    slownik = im_nazw_Resp(id=n, patient=rq.dict())
    wynik = slownik.dict()
    n += 1
    return wynik

class HelloResp(BaseModel):
    msg: str

@app.get("/patient/{pk}")
async def receive_patient(pk: int):
    if(pk in slownik_id.keys()):
        return slownik_id[pk]
    else: 
        raise HTTPException(status_code=204) 








