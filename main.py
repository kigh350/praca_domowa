from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel


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

n=0
@app.post("/patient", response_model=im_nazw_Resp)
def receive_patient(rq: im_nazw):
    global n
    n += 1
    slownik = im_nazw_Resp(id=n, patient=rq.dict())
    wynik = slownik.dict()
    return wynik












