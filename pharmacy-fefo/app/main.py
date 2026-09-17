from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Pharmacy FEFO Manager",
    description="Pharmacy inventory management using First-Expiry-First-Out",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "message": "Pharmacy FEFO API is running"
    }