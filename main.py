from typing import Dict

from fastapi import FastAPI

from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}


class HelloResp(BaseModel):
    msg: str

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



class GiveMePostRq(BaseModel):
    first_key: str

#class GiveMeSomethingResp(BaseModel):
#    received: Dict
#    constant_data: str = "python jest super"


#@app.post("/dej/mi/coś",  response_model=GiveMeSomethingResp)
#def receive_something(rq: GiveMeSomethingRq):
#    return GiveMeSomethingResp(received=rq.dict())

#class GiveMePost(BaseModel):
#    received: Dict
#    constant_data: str = "python jest super"

@app.post("/method")
def receive_post(rq: GiveMePostRq):
    return GiveMePostRq(received=rq)


