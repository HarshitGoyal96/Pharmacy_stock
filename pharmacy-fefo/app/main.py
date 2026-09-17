from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI(
    title="Pharmacy FEFO Manager",
    description="Pharmacy inventory management using First-Expiry-First-Out",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "Pharmacy FEFO API is running"
    }