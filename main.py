from typing import Dict
from fastapi import FastAPI, Request, Response, status
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    surename: str


app = FastAPI()
app.counter: int=0 # ustawiamy licznik na 0 
app.storage: Dict[int, Patient] = {}


@app.get("/")
def root():
    return {"message": "Witam Cie na mojej stronie"}

@app.get("/welcome")
def root():
    return {"message": "Witam Cie na mojej stronie"}


#zadanie z zajec
@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}

#moje rozwiazanie zad 2
#@app.get("/method")
#def read_item():
    #return {"method": "GET"}
#@app.post("/method")
#def read_item():
    #return {"method": "POST"}
#@app.delete("/method")
#def read_item():
    #return {"method": "DELETE"}
#@app.put("/method")
#def read_item():
    #return {"method": "PUT"}

# klasa pomocnicza 

@app.post("/patient")
def receive_patient(patient: Patient):
    resp = {"id": app.counter, "patint": patient}
    app.storage[app.counter]=patient
    app.counter += 1 
    return resp

@app.get("/patient/{pk}")
def receive_patient(pk: int):
    if(pk in app.storage):
        return app.storage.get(pk)
    return Response(status_code = status.HTTP_204_NO_CONTENT)




#class im_nazw(BaseModel):
    #name: str = "NAME"
    #surename: str = "SURENAME"
#class im_nazw_Resp(BaseModel):
    #id: int
    #patient: Dict

#class im_nazw_pat(BaseModel):
    #Dict    

#n=0
#lista=[n]
#slownik={}

#async def update_item(*, item: im_nazw):
    #global slownik
    #slownik = {"patient": item}
    #return slownik
