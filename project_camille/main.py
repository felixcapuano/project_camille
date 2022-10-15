import sqlite3
from pathlib import Path

from fastapi import Cookie, Depends, FastAPI, Query, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials


BASE_PATH = Path(__file__).resolve().parent

connection = sqlite3.connect(BASE_PATH / "main.db")
cursor = connection.cursor()

templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(openapi_url=None, redoc_url=None, docs_url=None)

security = HTTPBasic()

async def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.password != "qwerty" and credentials.username != "vilain":
        raise HTTPException(status_code=401, detail="Tu as échoué pour réessayer, tu peux rafraichire la page.")

@app.get("/", response_class=HTMLResponse, dependencies=[Depends(basic_auth)])
async def root(request: Request, logged: bool = Cookie(default=False, alias="Logged")):
    return templates.TemplateResponse("home.html", {"request": request, "logged": logged})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/form", response_class=RedirectResponse, dependencies=[Depends(basic_auth)])
async def login(username: str = Query(default=""), password: str = Query(default="")):

    # > ' OR '1'='1
    select = cursor.execute(f"SELECT username, password FROM users WHERE username='{username}' AND password='{password}'")
    is_user_exist = select.fetchone()

    headers = {"Set-Cookie": f"Logged={is_user_exist != None}; HttpOnly"}

    redirect = "/" if is_user_exist else "/login"

    return RedirectResponse(url=redirect, headers=headers)

@app.get("/logout", response_class=RedirectResponse, dependencies=[Depends(basic_auth)])
async def logout():
    headers = {"Set-Cookie": f"Logged={False}; HttpOnly"}
    return RedirectResponse(url="/", headers=headers)

@app.get("/{code}", response_class=HTMLResponse, dependencies=[Depends(basic_auth)])
async def easter_egg(request: Request, code: str):
    success = False
    if code == "25":
        success = True
    return templates.TemplateResponse("treasure.html", {"request": request, "success": success})