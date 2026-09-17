from pathlib import Path
from .auth_routes import router as auth_router
from fastapi import FastAPI, Request
from .medicine_routes import router as medicine_router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import Base, engine
from . import models


BASE_DIR = Path(__file__).resolve().parent


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Pharmacy FEFO Manager",
    description="Pharmacy inventory management using First-Expiry-First-Out",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(medicine_router)

# Templates
templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/api/health")
async def health_check():
    from sqlalchemy import text
    from .database import SessionLocal

    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "api": "running",
            "database": "connected",
            "message": "Pharmacy FEFO API and database are running"
        }

    except Exception as e:
        return {
            "status": "error",
            "api": "running",
            "database": "error",
            "message": str(e)
        }

    finally:
        db.close()