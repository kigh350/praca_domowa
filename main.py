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

class imie_nazwisko(BaseModel):
    name: str
    surename: str

N=0
@app.post("/patient", response_model=imie_nazwisko)
def read_item(rq: imie_nazwisko):
    N=N+1
    return {"id": N, "patient": {"name": imie_nazwisko.name, "surename": imie_nazwisko.surname}}







