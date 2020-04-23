from typing import Dict
from fastapi import Depends, FastAPI, Request, Response, HTTPException, status, Cookie
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from hashlib import sha256
from fastapi.templating import Jinja2Templates

class Patient(BaseModel):
    name: str
    surename: str


app = FastAPI()
security = HTTPBasic()
app.secret_key = "wUYwdjICbQP70WgUpRajUwxnGChAKmRtfQgYASazava4p5In7pZpFPggdB4JDjlv"
app.counter: int=0 # ustawiamy licznik na 0 
app.storage: Dict[int, Patient] = {}
templates = Jinja2Templates(directory="templates")
#app.patient={}
app.users={"trudnY":"PaC13Nt"}
app.sessions={}

@app.get("/")
def root():
    return {"message": "Witam Cie na mojej glownej stronie"}

def check_cookie(session_token: str = Cookie(None)):
    if session_token not in app.sessions:
        session_token = None
    return session_token

@app.get("/welcome")
def welcome(request: Request, response: Response, session_token: str = Depends(check_cookie)):
    if session_token is None: 
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Brak autoryzacji"
    username = app.sessions[session_token]
    return templates.TemplateResponse("welcome.html", {"request": request, "user": username})

# sprawdzenie poprawnosci loginu i zwrocenie tokena


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "trudnY")
    correct_password = secrets.compare_digest(credentials.password, "PaC13Nt")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret_key}", encoding='utf8')).hexdigest()
    app.sessions[session_token]=credentials.username
    return session_token

@app.post("/login")
def create_cookie(response: Response, session_token: str = Depends(get_current_username)):
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/welcome"
    response.set_cookie(key = "session_token", value=session_token)


@app.post("/logout")
def create_cookie(response: Response, session_token: str = Depends(check_cookie)):
    if session_token is None:                                               
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Brak autoryzacji"
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = "/"
    app.sessions.pop(session_token)


#zadanie z zajec
@app.api_route(path="/method", methods=["GET", "POST", "DELETE", "PUT", "OPTIONS"])
def read_request(request: Request):
    return {"method": request.method}


@app.post("/patient")
def receive_patient(patient: Patient, response: Response, session_token: str = Depends(check_cookie)):
    if session_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Brak autoryzacji"
    resp = {"id": app.counter, "patint": patient}
    pk = f"id_{app.counter}"
    app.storage[app.counter]=patient
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = f"/patient/{pk}"
    app.counter += 1 
    return resp

@app.get("/patient")
def pacjenci(response: Response, session_token: str=Depends(check_cookie)):
    if session_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Brak autoryzacji"
    if len(app.storage) > 0: 
        return app.storage
    response.status_code = status.HTTP_204_NO_CONTENT

@app.get("/patient/{pk}")
def receive_patient(pk: int, response: Response, session_token: str = Depends(check_cookie)):
    if session_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Brak autoryzacji"       
    if(pk in app.storage):
        return app.storage.get(pk)
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.delete("/patient/{pk}")
def usun_patient(pk: int, response: Response, session_token: str = Depends(check_cookie)):
    if session_token is None:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return "Brak autoryzacji"       
    app.storage.pop(pk, None)
    Response(status_code = status.HTTP_204_NO_CONTENT)




