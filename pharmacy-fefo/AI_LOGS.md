this is the task given to me can you do it my problem statement is 

Absolutely. We can build this end-to-end within the 2.5-hour constraint, and I can guide you from the problem statement all the way to a GitHub-ready submission.

From the assignment, your project needs:

Full-stack application
Database with real persistence
REST APIs
Usable frontend/UI
Registration + Login
Search
Pagination + Sorting
One-page landing page
README.md
REASONING.md
AI_LOGS.md
Public GitHub repository
Everything runnable in GitHub Codespaces
Send me your actual problem statement

Your message ended at:

"my problem statement is"

So paste the exact problem statement/story + twist assigned to you.

Once you send it, I'll help you build it in a 2.5-hour implementation strategy, including:

Choose the fastest suitable tech stack
Design the database schema
Define all required REST endpoints
Create the backend
Create the frontend
Implement authentication
Implement search, sorting & pagination
Create the landing page
Prepare README.md
Prepare REASONING.md
Tell you exactly what to put in AI_LOGS.md
Give you the Git commands for Codespaces
Help debug anything that breaks

For this kind of test, I'd prioritize working functionality over fancy UI. Think "small but complete product", not "trying to rebuild Amazon before the timer hits zero." 😄

Send the exact problem statement now, and we'll start with the architecture and implementation plan.

The storyline
A neighbourhood pharmacy stocks medicines in batches, each with its own expiry date. When they dispense a medicine they should use the batch that expires soonest first, and never dispense an expired batch. The pharmacist wants to know the sellable stock of a medicine (ignoring expired batches), gets asked ‘do we have paracetamol in date?’, and needs a heads-up on batches about to expire.
Build the pharmacy something so stock is always dispensed oldest-first and nothing expired goes out.
(Build it for any pharmacy. Get batches, first-expiry-first-out dispensing and the in-date stock count right first, then search and alerts.)

this is my problem statement give me what files to download as i am working in git codespace and give me from scratch

Analysis paused
give me a section at a time use python for development and related to it

Yes. We'll do it one section at a time, and I'll keep the entire project Python-based so you can build it quickly in GitHub Codespaces.

For a 2.5-hour assessment, I recommend:

Backend: Python + FastAPI
Database: SQLite
Frontend: HTML + CSS + JavaScript
ORM: SQLAlchemy
Authentication: JWT + bcrypt
API: REST
No React/Vite initially, because setting up a separate frontend wastes precious assessment time.

We'll build it in roughly this order:

🧱 Project setup
🗄️ Database + models
🔐 Registration + login
💊 Medicine/batch APIs
⚡ FEFO dispensing logic
🔎 Search + pagination + sorting
⏰ Expiry alerts
🎨 UI/dashboard
📄 README + REASONING
🧪 Testing + GitHub submission
SECTION 1: Project Setup
1. Create the project in Codespaces

Open your GitHub Codespace terminal and run:

mkdir pharmacy-fefo
cd pharmacy-fefo

Create the folders:

mkdir app
mkdir app/templates
mkdir app/static
mkdir app/static/css
mkdir app/static/js

Your structure should now be:

pharmacy-fefo/
│
├── app/
│   ├── templates/
│   └── static/
│       ├── css/
│       └── js/
│
└──
2. Create Python virtual environment

Run:

python -m venv venv

Activate it:

Linux/Codespaces
source venv/bin/activate

You should see something like:

(venv) vscode ➜ /workspaces/pharmacy-fefo $
3. Create requirements.txt

Run:

touch requirements.txt

Open it:

code requirements.txt

Put this inside:

fastapi
uvicorn[standard]
sqlalchemy
python-jose[cryptography]
passlib[bcrypt]
python-multipart
jinja2

Save it.

Then install everything:

pip install -r requirements.txt
4. Create app/main.py

Run:

touch app/main.py

Put this inside:

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
5. Create the first UI

Create:

touch app/templates/index.html

Put this inside:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Pharmacy FEFO Manager</title>

    <link
        rel="stylesheet"
        href="/static/css/style.css"
    >
</head>

<body>

    <header>
        <h1>💊 Pharmacy FEFO Manager</h1>

        <p>
            First-Expiry-First-Out inventory management
        </p>
    </header>

    <main>

        <section class="hero">

            <h2>
                Safe medicine inventory, batch by batch.
            </h2>

            <p>
                Track medicine batches, monitor expiry dates,
                and ensure the earliest valid batch is always
                dispensed first.
            </p>

            <button onclick="checkAPI()">
                Check API
            </button>

            <p id="api-status"></p>

        </section>

    </main>

    <script src="/static/js/app.js"></script>

</body>
</html>
6. Create CSS

Run:

touch app/static/css/style.css

Put:

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    color: #1f2937;
}

header {
    background: #2563eb;
    color: white;
    padding: 25px 8%;
}

header h1 {
    margin-bottom: 8px;
}

main {
    padding: 50px 8%;
}

.hero {
    background: white;
    padding: 40px;
    border-radius: 16px;
    max-width: 800px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.hero h2 {
    font-size: 32px;
    margin-bottom: 15px;
}

.hero p {
    line-height: 1.6;
    margin-bottom: 20px;
}

button {
    border: none;
    background: #2563eb;
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 15px;
}

button:hover {
    background: #1d4ed8;
}

#api-status {
    margin-top: 15px;
    font-weight: bold;
}
7. Create JavaScript

Run:

touch app/static/js/app.js

Put:

async function checkAPI() {
    const status = document.getElementById("api-status");

    try {
        const response = await fetch("/api/health");
        const data = await response.json();

        status.textContent = data.message;
    } catch (error) {
        status.textContent = "API connection failed";
        console.error(error);
    }
}
8. Run the application

From the project root:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

You should see:

Uvicorn running on http://0.0.0.0:8000

In Codespaces, click Open in Browser for port 8000.

You should see:

💊 Pharmacy FEFO Manager

and the Check API button.

Click it.

You should get:

Pharmacy FEFO API is running

9. Check FastAPI documentation

This is important because your assessment specifically requires REST APIs.

Open:

http://localhost:8000/docs

Codespaces will normally give you its forwarded URL.

You should see the Swagger interface.

Currently you'll have:

GET /
GET /api/health

Later we'll have things like:

POST   /api/auth/register
POST   /api/auth/login

GET    /api/medicines
POST   /api/medicines

GET    /api/medicines/{id}/batches
GET    /api/medicines/{id}/stock

POST   /api/medicines/{id}/dispense

GET    /api/alerts/expiring

That gives us the foundation for the entire application.

10. Final structure after Section 1

You should have:

pharmacy-fefo/
│
├── venv/
│
├── requirements.txt
│
└── app/
    │
    ├── main.py
    │
    ├── templates/
    │   └── index.html
    │
    └── static/
        │
        ├── css/
        │   └── style.css
        │
        └── js/
            └── app.js
Don't build anything else yet.

The next section is the important one: we'll create the SQLite database and design the schema around the pharmacy's actual business rules:

User
  ↓
Medicine
  ↓
Batch
 ├── batch number
 ├── quantity
 ├── expiry date
 └── medicine

And we'll make sure the database supports the key requirement:

Expired batches can exist in inventory records, but the dispensing system can never use them.

Once Section 1 is working, tell me "Section 2", and I'll give you only the database/model part with the exact Python files and commands.

it is showing nothing

That's actually useful. It means the database has not been created yet. No problem, we'll fix it now. 🛠️

The most likely reason is that database.py / models.py were not created or main.py is still the old version.

Let's do this carefully, with commands that you can copy-paste.

Step 1: Check your app folder

Run:

ls -la app

You should see:

__init__.py
main.py
database.py
models.py
templates

If database.py or models.py is missing, create them with:

touch app/database.py app/models.py
Step 2: Put the database code in database.py

Run:

code app/database.py

Delete anything inside and paste:

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./pharmacy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

Save with:

Ctrl + S
Step 3: Put the models in models.py

Run:

code app/models.py

Paste:

from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False,
        index=True
    )

    generic_name = Column(
        String(150),
        nullable=True
    )

    manufacturer = Column(
        String(150),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    batches = relationship(
        "Batch",
        back_populates="medicine",
        cascade="all, delete-orphan"
    )


class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)

    medicine_id = Column(
        Integer,
        ForeignKey("medicines.id"),
        nullable=False,
        index=True
    )

    batch_number = Column(
        String(100),
        nullable=False,
        index=True
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    expiry_date = Column(
        Date,
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    medicine = relationship(
        "Medicine",
        back_populates="batches"
    )

Save.

Step 4: Replace main.py

This is the most important part.

Run:

code app/main.py

Delete everything and paste:

from pathlib import Path

from fastapi import FastAPI, Request
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


# Templates
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

Save it.

Step 5: Check your files

Run:

ls -la app

You should now have:

__init__.py
main.py
database.py
models.py
templates
Step 6: Restart FastAPI

Stop your current server:

Ctrl + C

Then make sure you're in the project root:

pwd

It should be:

/workspaces/Pharmacy_stock/pharmacy-fefo

Now run:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Look for:

Application startup complete.
Step 7: NOW check the database

Open a second terminal while the server is running.

Run:

ls -lh pharmacy.db

You should now see something like:

-rw-r--r-- 1 vscode vscode 20K Sep 17 14:xx pharmacy.db

Then run:

python -c "import sqlite3; db=sqlite3.connect('pharmacy.db'); print(db.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()); db.close()"

You should get:

[('users',), ('medicines',), ('batches',)]

🎉 That means our database is working.

One important detail

Don't worry that the website itself doesn't show "Database connected."

The website isn't the database test.

Our actual verification is:

pharmacy.db exists
        ↓
SQLite opens
        ↓
users table exists
medicines table exists
batches table exists
        ↓
✅ DATABASE WORKING

And /api/health should now show:

{
  "status": "ok",
  "api": "running",
  "database": "connected",
  "message": "Pharmacy FEFO API and database are running"
}

Do these steps exactly and send me the output of:

ls -lh pharmacy.db

and

python -c "import sqlite3; db=sqlite3.connect('pharmacy.db'); print(db.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()); db.close()"

We'll stay on Section 2 until that works.

how to open new terminal in git codespace 

In GitHub Codespaces, you can open a new terminal in VS Code very easily.

Method 1: Keyboard shortcut

Press:

`Ctrl + Shift + ``

The backtick key is the key just below Esc and above Tab.

Method 2: Menu

At the top of the Codespace, click:

Terminal → New Terminal

You'll get something like:

TERMINAL

bash
@HarshitGoyal96 ➜ /workspaces/Pharmacy_stock/pharmacy-fefo (main) $

Your existing terminal can keep running:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

And the new terminal can be used for our database checks.

In the new terminal, run:
ls -lh pharmacy.db

Then:

python -c "import sqlite3; db=sqlite3.connect('pharmacy.db'); print(db.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()); db.close()"

Send me the output of those two commands. We'll verify the database before moving ahead.

this is the output

Perfect! ✅ Section 2 is successfully completed.

Your output confirms both things we needed:

1. Database exists
-rw-r--r-- 1 codespace codespace 48K Sep 17 09:34 pharmacy.db

✅ pharmacy.db exists.

2. All three tables exist

Your command returned:

[('users',), ('medicines',), ('batches',)]

So our database is:

pharmacy.db
│
├── users
├── medicines
└── batches

That's exactly what we wanted. 🎯

SECTION 3: User Registration + Login

Now we're going to implement authentication.

The flow will be:

Register
   ↓
Email + Password
   ↓
Password hashed with bcrypt
   ↓
Stored in SQLite
   ↓
Login
   ↓
JWT token
   ↓
Access protected pharmacy APIs

We'll keep this section focused only on authentication.

Step 1: Create auth.py

Run:

touch app/auth.py

Then:

code app/auth.py

Paste:

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext


SECRET_KEY = "pharmacy-fefo-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(user_id: int) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

Save it.

Step 2: Create authentication schemas

Create:

touch app/schemas.py

Open:

code app/schemas.py

Paste:

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
Important

We're using EmailStr, so install the email validation dependency:

pip install email-validator

Also add it to your requirements:

pip freeze > requirements.txt

This ensures your Codespace environment can be recreated later.

Step 3: Create authentication routes

Create:

touch app/auth_routes.py

Open it:

code app/auth_routes.py

Paste:

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import User
from .schemas import RegisterRequest, LoginRequest
from .auth import hash_password, verify_password, create_access_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful",
        "user_id": user.id
    }


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user.id)

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

Save.

Step 4: Connect authentication to FastAPI

Open:

code app/main.py

Add this import:

from .auth_routes import router as auth_router

Then after:

app = FastAPI(

and the complete FastAPI(...) configuration, add:

app.include_router(auth_router)

So that part should look like:

app = FastAPI(
    title="Pharmacy FEFO Manager",
    description="Pharmacy inventory management using First-Expiry-First-Out",
    version="1.0.0"
)

app.include_router(auth_router)
Step 5: Restart the server

Stop your existing server:

Ctrl + C

Then:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

You should get:

Application startup complete.
Step 6: Open Swagger

Go to:

/docs

You should now see:

Authentication

POST /api/auth/register
POST /api/auth/login

This is where we'll test registration and login.

Step 7: Test registration

Click:

POST /api/auth/register

Then:

Try it out

Use:

{
  "name": "Harshit",
  "email": "harshit@test.com",
  "password": "password123"
}

Click Execute.

You should receive something like:

{
  "message": "Registration successful",
  "user_id": 1
}
Step 8: Test login

Now select:

POST /api/auth/login

Use:

{
  "email": "harshit@test.com",
  "password": "password123"
}

You should receive:

{
  "message": "Login successful",
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Harshit",
    "email": "harshit@test.com"
  }
}

That long eyJ... string is your JWT access token.

Step 9: Verify the password is actually stored securely

Open a second terminal and run:

python -c "import sqlite3; db=sqlite3.connect('pharmacy.db'); print(db.execute('SELECT id,name,email,password_hash FROM users').fetchall()); db.close()"

You should see something resembling:

[
  (
    1,
    'Harshit',
    'harshit@test.com',
    '$2b$12$...'
  )
]

Notice that the password is not stored as:

password123

Instead, it looks like:

$2b$12$...

That's the bcrypt hash. 🔐

Stop here

Don't start the medicine APIs yet.

For Section 3, we only need these to work:

POST /api/auth/register    ✅
POST /api/auth/login       ✅
Password hashed            ✅
JWT generated              ✅
User stored in SQLite      ✅

If registration or login gives you an error, send me the exact error, and we'll fix it before proceeding to Section 4: Medicine + Batch REST APIs.