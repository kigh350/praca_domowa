from typing import Dict
from fastapi import Depends, FastAPI, Request, Response, HTTPException, status, Cookie
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import sqlite3
import json
from hashlib import sha256
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
#from fastapi.encoders import jsonable_encoder

class Patient(BaseModel):
    name: str
    surname: str


app = FastAPI()
security = HTTPBasic()
app.secret_key = "wUYwdjICbQP70WgUpRajUwxnGChAKmRtfQgYASazava4p5In7pZpFPggdB4JDjlv"
app.counter: int=0 # ustawiamy licznik na 0 
app.storage: Dict[int, Patient] = {}
templates = Jinja2Templates(directory="templates")
#app.patient={}
app.users={"trudnY":"PaC13Nt"}
app.sessions={}

# polaczenie i zamkniecie bazy danych
@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')

@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

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
    pk = f"id_{app.counter}"
    app.storage[app.counter]=patient
    #resp = {"id": app.counter, "patint": patient}
    response.status_code = status.HTTP_302_FOUND
    response.headers["Location"] = f"/patient/{app.counter}"
    app.counter += 1 
    return patient

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
    return Response(status_code = status.HTTP_204_NO_CONTENT)

# baza danych - praca domowa 4 

@app.get("/tracks")
async def tracks(page=0, per_page=10):
    app.db_connection.row_factory = sqlite3.Row
    tracks = app.db_connection.execute("SELECT * FROM tracks ORDER BY TrackId LIMIT :per_page OFFSET :per_page*:page", {'per_page': per_page, 'page': page}).fetchall()
    return tracks

@app.get("/tracks/composers/")
async def composer(composer_name: str, response: Response):
    app.db_connection.row_factory = lambda cursor, x: x[0]
    title = app.db_connection.execute("SELECT Name FROM tracks WHERE composer=:composer_name ORDER BY Name ", {'composer_name': composer_name}).fetchall()
    if len(title)>0: 
        return title
    err = {"detail": {"error": "nie znaleziono kompozytora"}}
    return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content=err)

class Album(BaseModel):
    title: str
    artist_id: int
        
@app.post("/albums")
async def albums_add(album: Album, response: Response):
#    album.artist_id = 100
    app.db_connection.row_factory = sqlite3.Row
    artist = app.db_connection.execute("SELECT artistid FROM artists where artistid=:artist_id", {'artist_id': album.artist_id}).fetchall()
    cursor = app.db_connection.execute(
        "INSERT INTO albums (title, artistId) VALUES (?, ?)", (album.title, album.artist_id)
        )
    app.db_connection.commit()
    new_album_id = cursor.lastrowid
    app.db_connection.row_factory = lambda cursor, x: x[:3]
    album_new = app.db_connection.execute(
    """SELECT albumid, title, artistid 
    FROM albums WHERE albumId = ?""",
    (new_album_id, )).fetchall()
    if len(artist)>0:
        response.status_code = status.HTTP_201_CREATED
        return {"AlbumId": cursor.lastrowid, "Title": album.title, "ArtistId": album.artist_id}
    err = {"detail": {"error": "nie znaleziono kompozytora"}}
    return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content=err)

@app.get("/albums/{albumid}")
async def album(albumid: int):
    app.db_connection.row_factory = sqlite3.Row
    album = app.db_connection.execute("SELECT * FROM albums WHERE albumid =:albumid", {'albumid': albumid,}).fetchone()
    return album


class Customer(BaseModel):
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None
    fax: str = None
    
@app.put("/customers/{cust_id}")
async def change_customers(cust_id: int, customer: Customer):
    app.db_connection.row_factory = sqlite3.Row
    cust = app.db_connection.execute("SELECT * FROM customers where customerid=:customer_id", {'customer_id': cust_id}).fetchall()
    if len(cust)==0:
        err = {"detail": {"error": "nie znaleziono klienta"}}
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content=err)
    update_customer = customer.dict(exclude_unset=True)
    values = list(update_customer.values())
    if len(values) != 0:
        values.append(cust_id)
        query = "UPDATE customers SET "
        for key, value in update_customer.items():
            key.capitalize()
            if key == "Postalcode":
                key = "PostalCode"
            query += f"{key}=?, "
        query = query[:-2]
        query += " WHERE CustomerId = ?"
        cursor = app.db_connection.execute(query, tuple(values))
        app.db_connection.commit()
    app.db_connection.row_factory = sqlite3.Row
    customer_new = app.db_connection.execute("SELECT * FROM customers WHERE CustomerId = ?",(cust_id, )).fetchone()
    return cust   




