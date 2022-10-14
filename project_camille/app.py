from select import select
import sqlite3
from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


BASE_PATH = Path(__file__).resolve().parent

connection = sqlite3.connect(BASE_PATH / "main.db")
cursor = connection.cursor()

templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(default=""), password: str = Form(default="")):

    select = cursor.execute(f"SELECT password FROM users WHERE username='{username}'")
    user_password = select.fetchone()
    if user_password:
        print("user found", user_password[0])
    else:
        print("user not found")

    if username == "vilain" and password == "toto":
        return "success"
    else:
        return "fail"

@app.get("/0{code}", response_class=HTMLResponse)
async def easter_egg(request: Request, code: str):
    if code == "2102":
        return templates.TemplateResponse("success.html", {"request": request})
    else:
        return templates.TemplateResponse("fail.html", {"request": request})