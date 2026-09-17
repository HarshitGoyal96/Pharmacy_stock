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

Step 3: Important distinction

If VS Code is showing a yellow/blue warning like:

.schemas could not be resolved

but this command:

python -c "from app.schemas import RegisterRequest, LoginRequest; print('Schemas OK')"

prints:

Schemas OK

then your code is fine. That's a VS Code/Pylance interpreter warning, not a Python runtime problem.

You can check your selected Python interpreter with:

Ctrl + Shift + P

then search:

Python: Select Interpreter

Choose the interpreter inside your project:

./venv/bin/python
Step 4: Test the actual server

Once the import works, start:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Then open:

/docs

You should see:

Authentication

POST /api/auth/register
POST /api/auth/login
Do this first

Run:

ls -la app

and send me the output. Don't change anything else yet. I'll tell you exactly what is missing.

it is saying that internal server error

Excellent. ✅ Registration is working.

That means this part is complete:

Registration
    ↓
FastAPI
    ↓
Validate email
    ↓
Hash password with bcrypt
    ↓
Save user in SQLite
    ↓
Registration successful ✅

Now let's finish Section 3 by testing login.

Step 1: Test Login

Go to:

/docs

Find:

POST /api/auth/login

Click Try it out.

Use the same credentials you registered with:

{
  "email": "admin2@pharmacy.com",
  "password": "password123"
}

Click Execute.

Expected response

You should get:

{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Pharmacy Admin",
    "email": "admin2@pharmacy.com"
  }
}

The important part is:

"access_token": "eyJ..."

That means JWT authentication is working.

Step 2: Test wrong password

Immediately test again with:

{
  "email": "admin2@pharmacy.com",
  "password": "wrongpassword"
}

You should get:

401 Unauthorized

with:

{
  "detail": "Invalid email or password"
}
Step 3: Verify the user in the database

In your second terminal:

python -c "import sqlite3; db=sqlite3.connect('pharmacy.db'); print(db.execute('SELECT id,name,email FROM users').fetchall()); db.close()"

You should see your registered user.

Once login works

Section 3 is finished. 🔐

Then we'll start the most important part of your assignment:

SECTION 4: Medicine & Batch APIs 💊

We'll create APIs to:

Add Medicine
       ↓
Add Batch
       ↓
Paracetamol
 ├── Batch A → 20 → expires Oct 2026
 ├── Batch B → 30 → expires Dec 2026
 └── Batch C → 10 → expired
       ↓
Calculate sellable stock
       ↓
Dispense using FEFO

And we'll make the API automatically reject expired batches.

First test the login endpoint. If it says "Login successful", tell me login successful and we'll start Section 4.

they both are showing successful

Perfect. 🔐 Section 3 is complete.

You now have:

✅ User registration
✅ Password hashing
✅ User stored in SQLite
✅ Login
✅ JWT token generation
✅ Invalid-password handling

Now we move to the actual pharmacy functionality.

SECTION 4: Medicine + Batch REST APIs 💊

This section will let the pharmacist:

Add a medicine
Add batches for that medicine
View batches
Calculate sellable stock
Keep expired stock out of sellable stock

We are not doing FEFO dispensing yet. We'll do that in Section 5.

Step 1: Create medicine_routes.py

Run:

touch app/medicine_routes.py

Then:

code app/medicine_routes.py

Paste this:

from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .database import get_db
from .models import Medicine, Batch


router = APIRouter(
    prefix="/api/medicines",
    tags=["Medicines"]
)


# -------------------------
# Request schemas
# -------------------------

class MedicineCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    generic_name: str | None = None
    manufacturer: str | None = None


class BatchCreate(BaseModel):
    batch_number: str = Field(min_length=1, max_length=100)
    quantity: int = Field(gt=0)
    expiry_date: date


# -------------------------
# Add medicine
# -------------------------

@router.post("/")
def create_medicine(
    data: MedicineCreate,
    db: Session = Depends(get_db)
):

    medicine = Medicine(
        name=data.name,
        generic_name=data.generic_name,
        manufacturer=data.manufacturer
    )

    db.add(medicine)
    db.commit()
    db.refresh(medicine)

    return {
        "message": "Medicine created successfully",
        "medicine": {
            "id": medicine.id,
            "name": medicine.name,
            "generic_name": medicine.generic_name,
            "manufacturer": medicine.manufacturer
        }
    }


# -------------------------
# Add batch
# -------------------------

@router.post("/{medicine_id}/batches")
def create_batch(
    medicine_id: int,
    data: BatchCreate,
    db: Session = Depends(get_db)
):

    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    batch = Batch(
        medicine_id=medicine_id,
        batch_number=data.batch_number,
        quantity=data.quantity,
        expiry_date=data.expiry_date
    )

    db.add(batch)
    db.commit()
    db.refresh(batch)

    return {
        "message": "Batch added successfully",
        "batch": {
            "id": batch.id,
            "medicine_id": batch.medicine_id,
            "batch_number": batch.batch_number,
            "quantity": batch.quantity,
            "expiry_date": batch.expiry_date
        }
    }


# -------------------------
# Get all batches
# -------------------------

@router.get("/{medicine_id}/batches")
def get_batches(
    medicine_id: int,
    db: Session = Depends(get_db)
):

    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    batches = (
        db.query(Batch)
        .filter(Batch.medicine_id == medicine_id)
        .order_by(Batch.expiry_date.asc())
        .all()
    )

    return {
        "medicine": medicine.name,
        "batches": [
            {
                "id": batch.id,
                "batch_number": batch.batch_number,
                "quantity": batch.quantity,
                "expiry_date": batch.expiry_date,
                "expired": batch.expiry_date < date.today()
            }
            for batch in batches
        ]
    }


# -------------------------
# Get sellable stock
# -------------------------

@router.get("/{medicine_id}/stock")
def get_sellable_stock(
    medicine_id: int,
    db: Session = Depends(get_db)
):

    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    today = date.today()

    valid_batches = (
        db.query(Batch)
        .filter(
            Batch.medicine_id == medicine_id,
            Batch.quantity > 0,
            Batch.expiry_date >= today
        )
        .all()
    )

    sellable_stock = sum(
        batch.quantity
        for batch in valid_batches
    )

    return {
        "medicine_id": medicine.id,
        "medicine": medicine.name,
        "sellable_stock": sellable_stock,
        "as_of": today,
        "valid_batches": len(valid_batches)
    }

Save it.

Step 2: Connect these routes to FastAPI

Open:

code app/main.py

Add this import:

from .medicine_routes import router as medicine_router

Then below:

app.include_router(auth_router)

add:

app.include_router(medicine_router)

So you should have:

app.include_router(auth_router)
app.include_router(medicine_router)

Save.

Step 3: Restart the server

Stop Uvicorn:

Ctrl + C

Start again:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

You should see:

Application startup complete.
Step 4: Open Swagger

Go to:

/docs

You should now see a new section:

Medicines

with:

POST /api/medicines/
POST /api/medicines/{medicine_id}/batches
GET  /api/medicines/{medicine_id}/batches
GET  /api/medicines/{medicine_id}/stock

That's our first real pharmacy API. 🎯

Step 5: Add Paracetamol

Open:

POST /api/medicines/

Click Try it out.

Enter:

{
  "name": "Paracetamol",
  "generic_name": "Paracetamol 500mg",
  "manufacturer": "ABC Pharma"
}

Click Execute.

Expected:

{
  "message": "Medicine created successfully",
  "medicine": {
    "id": 1,
    "name": "Paracetamol",
    "generic_name": "Paracetamol 500mg",
    "manufacturer": "ABC Pharma"
  }
}

Your medicine ID will probably be 1.

Step 6: Add the first batch

Open:

POST /api/medicines/{medicine_id}/batches

Enter:

medicine_id = 1

Body:

{
  "batch_number": "PARA001",
  "quantity": 50,
  "expiry_date": "2026-10-15"
}

Click Execute.

Expected:

{
  "message": "Batch added successfully",
  "batch": {
    "id": 1,
    "medicine_id": 1,
    "batch_number": "PARA001",
    "quantity": 50,
    "expiry_date": "2026-10-15"
  }
}
Step 7: Add another batch

Add:

{
  "batch_number": "PARA002",
  "quantity": 30,
  "expiry_date": "2026-12-20"
}

Now Paracetamol has:

PARA001 → 50 → 2026-10-15
PARA002 → 30 → 2026-12-20
Step 8: Add an expired batch

This is an important test for your assignment.

Add:

{
  "batch_number": "PARA003",
  "quantity": 100,
  "expiry_date": "2025-12-01"
}

Now the database contains:

┌──────────┬──────────┬────────────┐
│ Batch    │ Quantity │ Expiry     │
├──────────┼──────────┼────────────┤
│ PARA001  │ 50       │ 2026-10-15 │
│ PARA002  │ 30       │ 2026-12-20 │
│ PARA003  │ 100      │ 2025-12-01 │ ← EXPIRED
└──────────┴──────────┴────────────┘

Notice that we're not deleting expired stock.

That's intentional.

The pharmacy should retain the batch record, but the system must prevent it from being sold.

Step 9: Check sellable stock

Open:

GET /api/medicines/{medicine_id}/stock

Use:

medicine_id = 1

Expected:

{
  "medicine_id": 1,
  "medicine": "Paracetamol",
  "sellable_stock": 80,
  "valid_batches": 2
}
Why 80?

Because:

PARA001 = 50 ✅
PARA002 = 30 ✅
PARA003 = 100 ❌ expired

Therefore:

50 + 30 = 80

The expired 100 units are not included.

This directly satisfies one of the most important requirements:

Get the in-date stock count right.

Step 10: Check batches

Call:

GET /api/medicines/1/batches

You should get all three batches, sorted by expiry:

PARA003 → 2025-12-01 → expired
PARA001 → 2026-10-15 → valid
PARA002 → 2026-12-20 → valid

The response should mark the expired batch:

"expired": true

while the valid ones have:

"expired": false
🎯 Section 4 checkpoint

At this point we have:

                    PHARMACY
                       │
                       ▼
                  Paracetamol
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       PARA001      PARA002      PARA003
       50 units     30 units     100 units
       Oct 2026     Dec 2026     Dec 2025
          ✅            ✅            ❌
          └────────────┬────────────┘
                       ▼
                 Sellable = 80

Do these tests in Swagger now.

If you successfully get:

Medicine created successfully
Batch added successfully
Sellable stock = 80

tell me "Section 4 working".

Then we'll build Section 5: FEFO Dispensing, the centerpiece of the assignment. We'll test a dispense of, say, 60 Paracetamol, and the system will automatically consume the October batch before touching the December batch while completely ignoring the expired batch. 💊

section 4 working

Excellent. 🎯 Section 4 is complete.

Now we reach the centerpiece of your assignment.

SECTION 5: FEFO Dispensing 💊

The requirement says:

The batch that expires soonest should be used first, and expired batches must never be dispensed.

Our API will enforce both rules on the backend, so even if someone bypasses the UI, the server still protects the inventory.

The flow will be:

Dispense 60 Paracetamol
          ↓
Find valid batches only
          ↓
Sort by expiry date
          ↓
Earliest expiry first
          ↓
Deduct quantity
          ↓
Return exactly which batches were used

For your current test data:

PARA003   100   2025-12-01   ❌ expired
PARA001    50   2026-10-15   ✅
PARA002    30   2026-12-20   ✅

If we dispense 60:

PARA003 → 0 used       ❌ ignored
PARA001 → 50 used      ✅
PARA002 → 10 used      ✅

Remaining:

PARA001 → 0
PARA002 → 20
PARA003 → 100
Step 1: Add the FEFO endpoint

Open:

code app/medicine_routes.py

Go to the bottom of the file and add:

# -------------------------
# FEFO Dispensing
# -------------------------

class DispenseRequest(BaseModel):
    quantity: int = Field(gt=0)


@router.post("/{medicine_id}/dispense")
def dispense_medicine(
    medicine_id: int,
    data: DispenseRequest,
    db: Session = Depends(get_db)
):

    # Check that medicine exists
    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    today = date.today()

    # Get ONLY valid, non-expired batches.
    # Earliest expiry comes first.
    valid_batches = (
        db.query(Batch)
        .filter(
            Batch.medicine_id == medicine_id,
            Batch.quantity > 0,
            Batch.expiry_date >= today
        )
        .order_by(Batch.expiry_date.asc(), Batch.id.asc())
        .all()
    )

    available_stock = sum(
        batch.quantity
        for batch in valid_batches
    )

    # Do not partially dispense if there is
    # not enough valid stock.
    if data.quantity > available_stock:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Insufficient sellable stock",
                "requested": data.quantity,
                "available": available_stock
            }
        )

    remaining = data.quantity
    dispensed_from = []

    # Consume earliest-expiring valid batches first.
    for batch in valid_batches:

        if remaining == 0:
            break

        quantity_taken = min(
            batch.quantity,
            remaining
        )

        batch.quantity -= quantity_taken
        remaining -= quantity_taken

        dispensed_from.append({
            "batch_id": batch.id,
            "batch_number": batch.batch_number,
            "expiry_date": batch.expiry_date,
            "quantity_dispensed": quantity_taken,
            "remaining_in_batch": batch.quantity
        })

    # Commit all changes together.
    db.commit()

    return {
        "message": "Medicine dispensed successfully",
        "medicine": medicine.name,
        "quantity_dispensed": data.quantity,
        "dispensed_from": dispensed_from
    }

Save the file.

Step 2: Restart FastAPI

Your --reload server may reload automatically.

If it doesn't, stop it:

Ctrl + C

Then:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Wait for:

Application startup complete.
Step 3: Check Swagger

Open:

/docs

Under Medicines, you should now have:

POST /api/medicines/{medicine_id}/dispense

This is our FEFO endpoint.

Step 4: Test the actual FEFO rule

⚠️ Before testing, make sure your batches are still:

PARA001 → 50 → 2026-10-15
PARA002 → 30 → 2026-12-20
PARA003 → 100 → 2025-12-01

If you haven't dispensed anything yet, you're good.

Open:

POST /api/medicines/{medicine_id}/dispense

Use:

medicine_id = 1

Request body:

{
  "quantity": 60
}

Execute it.

Step 5: Expected response

You should get something similar to:

{
  "message": "Medicine dispensed successfully",
  "medicine": "Paracetamol",
  "quantity_dispensed": 60,
  "dispensed_from": [
    {
      "batch_id": 1,
      "batch_number": "PARA001",
      "expiry_date": "2026-10-15",
      "quantity_dispensed": 50,
      "remaining_in_batch": 0
    },
    {
      "batch_id": 2,
      "batch_number": "PARA002",
      "expiry_date": "2026-12-20",
      "quantity_dispensed": 10,
      "remaining_in_batch": 20
    }
  ]
}

Notice something very important:

PARA003 does NOT appear.

Even though it has:

100 units

it is expired, so the backend completely ignores it.

That's exactly the business rule.

Step 6: Verify the batches

Now call:

GET /api/medicines/1/batches

You should see approximately:

PARA003 → 100 → 2025-12-01 → expired
PARA001 →   0 → 2026-10-15 → valid
PARA002 →  20 → 2026-12-20 → valid
Step 7: Check sellable stock

Call:

GET /api/medicines/1/stock

Expected:

{
  "medicine_id": 1,
  "medicine": "Paracetamol",
  "sellable_stock": 20,
  "valid_batches": 1
}

Because:

PARA001 = 0
PARA002 = 20
PARA003 = 100 expired

Therefore:

0 + 20 = 20
Step 8: Test insufficient stock

This is another important edge case.

Try:

{
  "quantity": 100
}

You currently have only:

20 sellable units

The API should return:

400 Bad Request

with:

{
  "detail": {
    "message": "Insufficient sellable stock",
    "requested": 100,
    "available": 20
  }
}
Why this matters

We don't want this:

Dispense 20
then discover we needed 100

That would leave the inventory partially changed.

Instead, we check:

if data.quantity > available_stock:

before changing any batch.

So the request fails without reducing stock.

Step 9: One more important FEFO test

Now add a new batch for Paracetamol:

{
  "batch_number": "PARA004",
  "quantity": 15,
  "expiry_date": "2026-09-30"
}

Your valid stock becomes:

PARA004 → 15 → 2026-09-30
PARA002 → 20 → 2026-12-20

Now dispense:

{
  "quantity": 18
}

The expected allocation is:

PARA004 → 15
PARA002 → 3

Not:

PARA002 → 18

because PARA004 expires sooner.

That test demonstrates that the algorithm isn't merely choosing the first database record. It is actually following expiry-date ordering.

What you've built now

Your core pharmacy logic is becoming:

                    MEDICINE
                       │
                  Paracetamol
                       │
          ┌────────────┼────────────┐
          │            │            │
       PARA003      PARA001      PARA002
       2025-12      2026-10      2026-12
       100 units     50 units     30 units
          ❌            ✅            ✅
       expired
                       │
                       ▼
                 SELLABLE STOCK
                       │
                       ▼
                 FEFO SORTING
                       │
                       ▼
              Earliest expiry first
                       │
                       ▼
                  DISPENSE
Section 5 checklist

You should now be able to demonstrate:

✅ Expired batches are never selected
✅ Earliest valid expiry is selected first
✅ One dispense can consume multiple batches
✅ Batch quantities are updated
✅ Sellable stock updates automatically
✅ Insufficient stock is rejected
✅ API returns exactly which batches were used
One small technical improvement we'll make later

We'll eventually put the dispensing operation inside a proper database transaction so multiple quantity updates are atomic even under failures/concurrent requests. For the assessment, the current pre-check + commit is enough to demonstrate the business rule, but we'll harden it before final submission.

Do the 60-unit test first. If the response shows PARA001 = 50 and PARA002 = 10, tell me "FEFO working" and we'll move to Section 6: Search + Pagination + Sorting. 🔎

Perfect. 🚀 FEFO is the most important business rule, and it's working.

SECTION 6: Search + Pagination + Sorting 🔎

Now we'll build the pharmacist's medicine lookup.

The API will support:

GET /api/medicines

with:

🔎 Search by medicine name
📄 Pagination
↕️ Sorting
💊 Sellable stock count
🚫 Expired stock excluded from stock count

For example:

/api/medicines?search=para&page=1&page_size=10&sort_by=name&order=asc
Step 1: Replace GET /api/medicines

Open:

code app/medicine_routes.py

At the top, make sure your imports look like this:

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import get_db
from .models import Medicine, Batch

Now add this endpoint to medicine_routes.py:

@router.get("/")
def get_medicines(
    search: str | None = Query(
        default=None,
        description="Search medicine by name"
    ),
    page: int = Query(
        default=1,
        ge=1
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100
    ),
    sort_by: str = Query(
        default="name"
    ),
    order: str = Query(
        default="asc"
    ),
    db: Session = Depends(get_db)
):

    today = date.today()

    # -------------------------
    # Search
    # -------------------------

    query = (
        db.query(
            Medicine,
            func.coalesce(
                func.sum(
                    Batch.quantity
                ).filter(
                    Batch.quantity > 0,
                    Batch.expiry_date >= today
                ),
                0
            ).label("sellable_stock")
        )
        .outerjoin(
            Batch,
            Medicine.id == Batch.medicine_id
        )
        .group_by(Medicine.id)
    )

    if search:
        query = query.filter(
            Medicine.name.ilike(f"%{search}%")
        )

    # -------------------------
    # Sorting
    # -------------------------

    if sort_by == "stock":
        sort_column = func.coalesce(
            func.sum(
                Batch.quantity
            ).filter(
                Batch.quantity > 0,
                Batch.expiry_date >= today
            ),
            0
        )
    else:
        sort_column = Medicine.name

    if order.lower() == "desc":
        query = query.order_by(
            sort_column.desc()
        )
    else:
        query = query.order_by(
            sort_column.asc()
        )

    # -------------------------
    # Total count
    # -------------------------

    total = query.count()

    # -------------------------
    # Pagination
    # -------------------------

    offset = (page - 1) * page_size

    medicines = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total_pages = (
        (total + page_size - 1)
        // page_size
    )

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "medicines": [
            {
                "id": medicine.id,
                "name": medicine.name,
                "generic_name": medicine.generic_name,
                "manufacturer": medicine.manufacturer,
                "sellable_stock": int(sellable_stock or 0)
            }
            for medicine, sellable_stock in medicines
        ]
    }

Save the file.

Step 2: Restart the server

If --reload doesn't automatically reload:

Ctrl + C

Then:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Step 3: Check Swagger

Open:

/docs

Under Medicines, you should now see:

GET /api/medicines/

It should show parameters:

search
page
page_size
sort_by
order
Step 4: Test without search

Click:

GET /api/medicines/

Then Try it out → Execute.

You should get something similar to:

{
  "page": 1,
  "page_size": 10,
  "total": 1,
  "total_pages": 1,
  "medicines": [
    {
      "id": 1,
      "name": "Paracetamol",
      "generic_name": "Paracetamol 500mg",
      "manufacturer": "ABC Pharma",
      "sellable_stock": 20
    }
  ]
}

Your stock number may differ depending on what you dispensed.

Step 5: Test search

Set:

search = para

Leave:

page = 1
page_size = 10
sort_by = name
order = asc

Execute.

It should return:

{
  "medicines": [
    {
      "id": 1,
      "name": "Paracetamol",
      ...
    }
  ]
}

Now try:

search = xyz

You should get:

{
  "total": 0,
  "medicines": []
}

This demonstrates the search functionality.

Step 6: Test sorting

You can sort by:

sort_by=name

or:

sort_by=stock

For example:

sort_by=stock
order=desc

will put medicines with greater sellable stock first.

And:

sort_by=name
order=asc

sorts alphabetically.

Step 7: Test pagination properly

Right now you only have one medicine, so let's create a few more.

Use:

POST /api/medicines/

Create:

Medicine 2
{
  "name": "Ibuprofen",
  "generic_name": "Ibuprofen 400mg",
  "manufacturer": "Health Pharma"
}
Medicine 3
{
  "name": "Amoxicillin",
  "generic_name": "Amoxicillin 500mg",
  "manufacturer": "MediCare"
}
Medicine 4
{
  "name": "Cetirizine",
  "generic_name": "Cetirizine 10mg",
  "manufacturer": "ABC Pharma"
}
Step 8: Add stock to them

For Ibuprofen, assuming ID 2:

{
  "batch_number": "IBU001",
  "quantity": 40,
  "expiry_date": "2027-01-15"
}

For Amoxicillin, ID 3:

{
  "batch_number": "AMX001",
  "quantity": 60,
  "expiry_date": "2027-03-20"
}

For Cetirizine, ID 4:

{
  "batch_number": "CET001",
  "quantity": 25,
  "expiry_date": "2027-02-10"
}

Now you have:

Paracetamol  → 20
Ibuprofen    → 40
Amoxicillin  → 60
Cetirizine   → 25
Step 9: Test pagination

Call:

GET /api/medicines/

with:

page = 1
page_size = 2

Expected:

{
  "page": 1,
  "page_size": 2,
  "total": 4,
  "total_pages": 2,
  "medicines": [
    ...
  ]
}

Then:

page = 2
page_size = 2

You should receive the remaining two medicines.

So the API is now doing:

4 medicines
     ↓
page_size = 2
     ↓
┌──────────────┐
│ Page 1       │
│ Medicine 1   │
│ Medicine 2   │
└──────────────┘

┌──────────────┐
│ Page 2       │
│ Medicine 3   │
│ Medicine 4   │
└──────────────┘
Step 10: Verify expired stock is excluded

This is an important connection between Sections 4, 5 and 6.

Add an expired batch to Ibuprofen:

{
  "batch_number": "IBU-EXPIRED",
  "quantity": 500,
  "expiry_date": "2025-01-01"
}

Ibuprofen now has:

IBU001       → 40 → 2027-01-15 ✅
IBU-EXPIRED  → 500 → 2025-01-01 ❌

Call:

GET /api/medicines/

Ibuprofen should still show:

"sellable_stock": 40

not:

540

That's a very nice demonstration for your evaluator because it shows the stock calculation consistently respects the core pharmacy rule.

🎯 Section 6 complete when these work

You should be able to demonstrate:

✅ Search
✅ Pagination
✅ Sorting by name
✅ Sorting by stock
✅ Sellable stock
✅ Expired stock excluded

Your backend is now becoming a proper REST inventory system:

             Pharmacy API
                  │
       ┌──────────┼──────────┐
       │          │          │
    Auth      Medicines    Alerts
       │          │
       │      ┌───┴────┐
       │      │        │
       │    Batches   Stock
       │               │
       │             FEFO
       │               │
       └───────────────┘

Do the search + pagination tests first. If GET /api/medicines/ works correctly, tell me "Section 6 working" and we'll build Section 7: Expiry Alerts, where the pharmacist gets a list of batches that are approaching expiry. ⏰

saying query is not defined in new route

showing this

That's because the Register button depends on showRegister(), and our app.js doesn't have that function yet. The HTML is fine.

Let's fix this now.

Step 8.4: Add the frontend JavaScript

Open:

app/static/js/app.js

Replace everything with this:

// ================================
// AUTH TABS
// ================================

function showLogin() {
    document.getElementById("login-form").style.display = "flex";
    document.getElementById("register-form").style.display = "none";

    document.getElementById("login-tab").classList.add("active");
    document.getElementById("register-tab").classList.remove("active");

    document.getElementById("auth-message").textContent = "";
}


function showRegister() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("register-form").style.display = "flex";

    document.getElementById("login-tab").classList.remove("active");
    document.getElementById("register-tab").classList.add("active");

    document.getElementById("auth-message").textContent = "";
}


// ================================
// REGISTER
// ================================

document
    .getElementById("register-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const name = document.getElementById("register-name").value;
        const email = document.getElementById("register-email").value;
        const password = document.getElementById("register-password").value;

        const message = document.getElementById("auth-message");

        try {

            const response = await fetch("/api/auth/register", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                message.textContent = data.detail || "Registration failed";
                message.style.color = "red";
                return;
            }

            message.textContent = "Registration successful! Please login.";
            message.style.color = "green";

            document.getElementById("register-form").reset();

            setTimeout(() => {
                showLogin();
            }, 1000);

        } catch (error) {

            console.error(error);

            message.textContent = "Unable to connect to server.";
            message.style.color = "red";
        }
    });


// ================================
// LOGIN
// ================================

document
    .getElementById("login-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const email = document.getElementById("login-email").value;
        const password = document.getElementById("login-password").value;

        const message = document.getElementById("auth-message");

        try {

            const response = await fetch("/api/auth/login", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await response.json();

            if (!response.ok) {
                message.textContent = data.detail || "Login failed";
                message.style.color = "red";
                return;
            }

            // Save authentication information
            localStorage.setItem(
                "access_token",
                data.access_token
            );

            localStorage.setItem(
                "user",
                JSON.stringify(data.user)
            );

            showDashboard(data.user);

        } catch (error) {

            console.error(error);

            message.textContent = "Unable to connect to server.";
            message.style.color = "red";
        }
    });


// ================================
// SHOW DASHBOARD
// ================================

function showDashboard(user) {

    document.getElementById("auth-section").style.display = "none";

    document.getElementById("dashboard").style.display = "block";

    document.getElementById("welcome-user").textContent =
        `Welcome, ${user.name}`;

    loadMedicines();
    loadAlerts();
}


// ================================
// LOGOUT
// ================================

function logout() {

    localStorage.removeItem("access_token");
    localStorage.removeItem("user");

    document.getElementById("dashboard").style.display = "none";

    document.getElementById("auth-section").style.display = "flex";

    showLogin();
}


// ================================
// MEDICINES
// ================================

let currentPage = 1;
const pageSize = 10;
let totalPages = 1;


async function loadMedicines() {

    const search =
        document.getElementById("search-input").value;

    const sortBy =
        document.getElementById("sort-by").value;

    const sortOrder =
        document.getElementById("sort-order").value;

    const url =
        `/api/medicines/?search=${encodeURIComponent(search)}` +
        `&page=${currentPage}` +
        `&page_size=${pageSize}` +
        `&sort_by=${sortBy}` +
        `&order=${sortOrder}`;

    try {

        const response = await fetch(url);

        const data = await response.json();

        if (!response.ok) {
            console.error(data);
            return;
        }

        totalPages = data.total_pages || 1;

        const table =
            document.getElementById("medicine-table");

        table.innerHTML = "";

        if (data.medicines.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align:center;">
                        No medicines found
                    </td>
                </tr>
            `;

        } else {

            data.medicines.forEach(medicine => {

                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${medicine.id}</td>

                    <td>
                        <strong>${medicine.name}</strong>
                    </td>

                    <td>
                        ${medicine.generic_name || "-"}
                    </td>

                    <td>
                        ${medicine.manufacturer || "-"}
                    </td>

                    <td class="stock">
                        ${medicine.sellable_stock}
                    </td>

                    <td>
                        <button
                            class="action-btn"
                            onclick="viewBatches(${medicine.id})"
                        >
                            View Batches
                        </button>
                    </td>
                `;

                table.appendChild(row);
            });
        }

        document.getElementById("page-info").textContent =
            `Page ${data.page} of ${totalPages}`;

    } catch (error) {

        console.error("Error loading medicines:", error);
    }
}


// ================================
// PAGINATION
// ================================

function nextPage() {

    if (currentPage < totalPages) {
        currentPage++;
        loadMedicines();
    }
}


function previousPage() {

    if (currentPage > 1) {
        currentPage--;
        loadMedicines();
    }
}


// ================================
// EXPIRY ALERTS
// ================================

async function loadAlerts() {

    const container =
        document.getElementById("alerts-container");

    try {

        const response =
            await fetch("/api/medicines/alerts/expiring?days=30");

        const data = await response.json();

        if (!response.ok) {
            container.textContent = "Unable to load alerts.";
            return;
        }

        if (data.alerts.length === 0) {

            container.innerHTML = `
                <div class="no-alerts">
                    ✓ No batches are expiring within 30 days.
                </div>
            `;

            return;
        }

        container.innerHTML = "";

        data.alerts.forEach(alert => {

            const item = document.createElement("div");

            item.className = "alert-item";

            item.innerHTML = `
                <strong>${alert.medicine}</strong>

                <br>

                Batch:
                ${alert.batch_number}

                <br>

                Quantity:
                ${alert.quantity}

                <br>

                Expiry:
                ${alert.expiry_date}

                <br>

                <strong>
                    ${alert.days_until_expiry} days remaining
                </strong>
            `;

            container.appendChild(item);
        });

    } catch (error) {

        console.error("Error loading alerts:", error);

        container.textContent =
            "Unable to connect to server.";
    }
}


// ================================
// MEDICINE MODAL
// ================================

function openMedicineForm() {

    document.getElementById("medicine-modal").style.display = "flex";
}


function closeMedicineForm() {

    document.getElementById("medicine-modal").style.display = "none";
}


// ================================
// ADD MEDICINE
// ================================

document
    .getElementById("medicine-form")
    .addEventListener("submit", async function(event) {

        event.preventDefault();

        const name =
            document.getElementById("medicine-name").value;

        const genericName =
            document.getElementById("generic-name").value;

        const manufacturer =
            document.getElementById("manufacturer").value;

        const message =
            document.getElementById("medicine-message");

        try {

            const response = await fetch("/api/medicines/", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name: name,
                    generic_name: genericName || null,
                    manufacturer: manufacturer || null
                })
            });

            const data = await response.json();

            if (!response.ok) {

                message.textContent =
                    data.detail || "Unable to add medicine";

                message.style.color = "red";

                return;
            }

            message.textContent =
                "Medicine added successfully!";

            message.style.color = "green";

            document
                .getElementById("medicine-form")
                .reset();

            loadMedicines();

            setTimeout(() => {
                closeMedicineForm();
                message.textContent = "";
            }, 1000);

        } catch (error) {

            console.error(error);

            message.textContent =
                "Unable to connect to server.";

            message.style.color = "red";
        }
    });


// ================================
// VIEW BATCHES
// ================================

async function viewBatches(medicineId) {

    try {

        const response =
            await fetch(
                `/api/medicines/${medicineId}/batches`
            );

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "Unable to load batches");
            return;
        }

        let message =
            `${data.medicine} Batches\n\n`;

        data.batches.forEach(batch => {

            message +=
                `Batch: ${batch.batch_number}\n` +
                `Quantity: ${batch.quantity}\n` +
                `Expiry: ${batch.expiry_date}\n` +
                `Expired: ${batch.expired ? "Yes" : "No"}\n\n`;
        });

        if (data.batches.length === 0) {
            message += "No batches found.";
        }

        alert(message);

    } catch (error) {

        console.error(error);

        alert("Unable to connect to server.");
    }
}


// ================================
// AUTO LOGIN
// ================================

window.addEventListener("DOMContentLoaded", () => {

    const token =
        localStorage.getItem("access_token");

    const userString =
        localStorage.getItem("user");

    if (token && userString) {

        try {

            const user = JSON.parse(userString);

            showDashboard(user);

        } catch (error) {

            logout();
        }
    }

});
Step 8.5: Refresh

Save the file, then in the browser press:

Ctrl + Shift + R

Now click:

Register

The login form should disappear and you should see:

Full Name
Email
Password

Create Account
Then test registration

Use a new email, for example:

Name: Test Pharmacist
Email: pharmacist@test.com
Password: test12345

Click Create Account.

You should see:

Registration successful! Please login.

Then it should automatically switch back to Login.

Important

If clicking Register still does nothing, open the browser developer console:

F12 → Console

and send me the red error message you see.

Once Register works, we'll test Login → Dashboard, then connect the medicine inventory to the UI.

now login and register both working

Perfect. 🔐✅ Section 8 authentication is working.

We now have:

✅ Registration
✅ Login
✅ JWT token generation
✅ Token stored in browser
✅ Logout
✅ Dashboard loading after login
✅ Medicine API connected
✅ Expiry alerts API connected
Next: Step 8.6, test the dashboard

After logging in, you should see:

🚨 Expiry Alerts

Batches expiring soon

💊 Medicines

Search box
Sort by name/stock
Medicine table
Pagination
Add Medicine

If the dashboard appears but the medicine table is empty, that's okay if you haven't added medicines through the current database.

Try:

Click + Add Medicine

Add:

Name: Ibuprofen
Generic Name: Ibuprofen
Manufacturer: ABC Pharma
Click Add Medicine
Check whether Ibuprofen appears in the table.
One thing we need to fix next

Our medicine APIs currently don't send the JWT token, so technically the inventory endpoints aren't protected by login yet.

We'll handle that after confirming the dashboard works.

Tell me what happens after login:

Does the dashboard appear?
Does the medicine table show your existing Paracetamol?
Does Add Medicine work?

Then we'll continue with the next section. 🚀

Excellent. ✅ Section 9: Batch Management + FEFO Dispensing is complete.

Now we should make the application more secure before final polish.

Section 10: Protect Medicine APIs with JWT 🔐

Currently, registration/login works and generates a JWT, but someone could still directly call:

POST /api/medicines/
POST /api/medicines/{id}/batches
POST /api/medicines/{id}/dispense
GET /api/medicines/

without logging in.

We'll fix that now.

Step 10.1: Create the authentication dependency

Open:

app/auth.py

Replace it with:

from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from .models import User


SECRET_KEY = "pharmacy-fefo-secret-key-change-this"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


def create_access_token(user_id: int) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
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


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token"
        )

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
Step 10.2: Protect the medicine router

Open:

app/medicine_routes.py

Change this:

from fastapi import APIRouter, Depends, HTTPException, Query

to:

from fastapi import APIRouter, Depends, HTTPException, Query

That line actually stays the same.

Then add:

from .auth import get_current_user

So your imports include:

from .database import get_db
from .models import Medicine, Batch
from .auth import get_current_user

Now change:

router = APIRouter(
    prefix="/api/medicines",
    tags=["Medicines"]
)

to:

router = APIRouter(
    prefix="/api/medicines",
    tags=["Medicines"],
    dependencies=[Depends(get_current_user)]
)

That's it.

Because we're putting the dependency on the router, all medicine endpoints are now protected:

GET    /api/medicines/
POST   /api/medicines/
GET    /api/medicines/{id}/batches
POST   /api/medicines/{id}/batches
GET    /api/medicines/{id}/stock
POST   /api/medicines/{id}/dispense
GET    /api/medicines/alerts/expiring

Authentication endpoints remain public:

POST /api/auth/register
POST /api/auth/login

That's exactly what we want.

Step 10.3: Update frontend requests

Now the frontend needs to send the JWT.

Open:

app/static/js/app.js

At the top, add:

function getAuthHeaders() {

    const token =
        localStorage.getItem("access_token");

    return {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
    };
}

Then update your medicine API requests.

loadMedicines()

Change:

const response = await fetch(url);

to:

const response = await fetch(
    url,
    {
        headers: getAuthHeaders()
    }
);
loadAlerts()

Change:

const response =
    await fetch("/api/medicines/alerts/expiring?days=30");

to:

const response =
    await fetch(
        "/api/medicines/alerts/expiring?days=30",
        {
            headers: getAuthHeaders()
        }
    );
viewBatches()

Change:

const response =
    await fetch(
        `/api/medicines/${medicineId}/batches`
    );

to:

const response =
    await fetch(
        `/api/medicines/${medicineId}/batches`,
        {
            headers: getAuthHeaders()
        }
    );
Add Medicine

Find:

headers: {
    "Content-Type": "application/json"
},

Replace it with:

headers: getAuthHeaders(),
Add Batch

Again replace:

headers: {
    "Content-Type": "application/json"
},

with:

headers: getAuthHeaders(),
Dispense

Do the same:

headers: getAuthHeaders(),
Step 10.4: Test authentication

Restart the server if necessary:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Then:

Refresh the browser.
Login.
Check that the dashboard still loads.
Search medicines.
Add a medicine.
Add a batch.
View batches.
Dispense.

Everything should still work.

Extra security test

Open Swagger:

/docs

Try:

GET /api/medicines/

without authorization.

It should now return:

401 Unauthorized

Then use the frontend after login, where the JWT is automatically supplied.

Why we're doing this

Our application now has a proper flow:

                ┌──────────────┐
                │   Register   │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │    Login     │
                └──────┬───────┘
                       ↓
                  JWT Token
                       ↓
             ┌──────────────────┐
             │   Dashboard      │
             └────────┬─────────┘
                      ↓
          ┌───────────────────────┐
          │ Authenticated APIs    │
          └───────────┬───────────┘
                      ↓
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
   Medicines       Batches        Dispensing
       ↓              ↓              ↓
    Search          Stock          FEFO
       ↓              ↓              ↓
   Pagination      Expiry       No expired
    Sorting         Alerts       dispensing
Section 10 completion criteria

You should have:

✅ Unauthenticated medicine API → 401
✅ Logged-in dashboard → works
✅ Search → works
✅ Add medicine → works
✅ Add batch → works
✅ View batches → works
✅ Dispense → works
✅ FEFO → still works
✅ Expiry alerts → still work

Once these pass, tell me "Section 10 done".

Then we'll move into the final UI/polish section, followed by the required README.md, REASONING.md, AI_LOGS.md, .gitignore, final testing, and GitHub submission. 🚀

Now lets move to the next section

Absolutely. Since Section 10 is done, let's move to the next major section.

Section 11: Professional Dashboard UI 🎨💊

The functionality is already working. Now we'll make the application look like a real pharmacy inventory system rather than an API project with a browser attached.

Section 11 will add
📊 Dashboard summary cards
💊 Total medicines
📦 Total sellable stock
🚨 Expiring batches count
🔎 Cleaner search/filter area
📋 Better medicine cards/table
🟢🟠🔴 Stock/expiry indicators
📱 Better responsive layout
✨ Cleaner buttons and spacing

We won't change your backend in this section.

Step 11.1: Update the dashboard HTML

Open:

app/templates/index.html

Find:

<main class="dashboard-container">

Immediately after it, add:

<!-- DASHBOARD SUMMARY -->

<div class="summary-grid">

    <div class="summary-card">

        <div class="summary-icon">
            💊
        </div>

        <div>
            <p>Total Medicines</p>
            <h2 id="total-medicines">0</h2>
        </div>

    </div>


    <div class="summary-card">

        <div class="summary-icon">
            📦
        </div>

        <div>
            <p>Sellable Stock</p>
            <h2 id="total-stock">0</h2>
        </div>

    </div>


    <div class="summary-card warning">

        <div class="summary-icon">
            🚨
        </div>

        <div>
            <p>Expiring Soon</p>
            <h2 id="expiring-count">0</h2>
        </div>

    </div>

</div>

So the beginning of your main section becomes:

<main class="dashboard-container">

    <!-- DASHBOARD SUMMARY -->

    <div class="summary-grid">

        ...
        
    </div>

    <!-- ALERTS -->

    <div class="section-card alert-card">
Step 11.2: Improve the medicine controls

Find this:

<div class="controls">

Replace the entire controls block with:

<div class="controls">

    <div class="search-box">

        🔎

        <input
            type="text"
            id="search-input"
            placeholder="Search medicine..."
            oninput="loadMedicines()"
        >

    </div>


    <select
        id="sort-by"
        onchange="loadMedicines()"
    >

        <option value="name">
            Sort by Name
        </option>

        <option value="stock">
            Sort by Stock
        </option>

    </select>


    <select
        id="sort-order"
        onchange="loadMedicines()"
    >

        <option value="asc">
            Ascending
        </option>

        <option value="desc">
            Descending
        </option>

    </select>

</div>
Step 11.3: Add dashboard CSS

Open:

app/static/css/style.css

Add this at the bottom:

/* =========================
   SUMMARY CARDS
========================= */

.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 25px;
}

.summary-card {
    background: white;
    padding: 22px;
    border-radius: 14px;

    display: flex;
    align-items: center;
    gap: 18px;

    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.06);

    border-left: 5px solid #2563eb;
}

.summary-card.warning {
    border-left-color: #f59e0b;
}

.summary-icon {
    width: 50px;
    height: 50px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #eff6ff;

    border-radius: 12px;

    font-size: 25px;
}

.summary-card p {
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 4px;
}

.summary-card h2 {
    font-size: 26px;
    color: #1f2937;
}


/* =========================
   SEARCH BOX
========================= */

.search-box {
    display: flex;
    align-items: center;

    background: white;

    border: 1px solid #d1d5db;

    border-radius: 8px;

    padding-left: 12px;

    overflow: hidden;
}

.search-box input {
    border: none;
    box-shadow: none;
}

.search-box input:focus {
    border: none;
    box-shadow: none;
}


/* =========================
   TABLE ACTIONS
========================= */

.action-btn {
    margin: 3px;
}

.action-btn:hover {
    transform: translateY(-1px);
}


/* =========================
   EMPTY STATE
========================= */

.empty-state {
    text-align: center;
    padding: 35px;
    color: #6b7280;
}

.empty-state-icon {
    font-size: 40px;
    margin-bottom: 10px;
}


/* =========================
   MOBILE DASHBOARD
========================= */

@media (max-width: 800px) {

    .summary-grid {
        grid-template-columns: 1fr;
    }

    .navbar {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }

    .navbar button {
        align-self: flex-end;
    }

}
Step 11.4: Update the JavaScript summary

Open:

app/static/js/app.js

Inside loadMedicines(), after:

totalPages = data.total_pages || 1;

add:

document.getElementById(
    "total-medicines"
).textContent = data.total;

Then we need to calculate total sellable stock.

Add:

const totalStock = data.medicines.reduce(
    (total, medicine) =>
        total + medicine.sellable_stock,
    0
);

document.getElementById(
    "total-stock"
).textContent = totalStock;
Important

Because pagination only returns the current page, this stock number represents the stock on the current page, not the entire pharmacy.

So don't worry if it looks different when you change pages. We'll make this globally accurate in a later API improvement.

Step 11.5: Update expiry count

Inside loadAlerts(), after:

const data = await response.json();

add:

document.getElementById(
    "expiring-count"
).textContent = data.count;
Step 11.6: Improve empty medicine display

Inside loadMedicines(), find:

if (data.medicines.length === 0) {

    table.innerHTML = `
        <tr>
            <td colspan="6" style="text-align:center;">
                No medicines found
            </td>
        </tr>
    `;

}

Replace it with:

if (data.medicines.length === 0) {

    table.innerHTML = `
        <tr>
            <td colspan="6">

                <div class="empty-state">

                    <div class="empty-state-icon">
                        💊
                    </div>

                    <strong>
                        No medicines found
                    </strong>

                    <p>
                        Try another search or add a new medicine.
                    </p>

                </div>

            </td>
        </tr>
    `;

}
Step 11.7: Add stock status

Find:

<td class="stock">
    ${medicine.sellable_stock}
</td>

Replace it with:

<td>

    <span
        class="stock-badge ${
            medicine.sellable_stock > 0
                ? "in-stock"
                : "out-stock"
        }"
    >

        ${
            medicine.sellable_stock > 0
                ? "● "
                : "● "
        }

        ${medicine.sellable_stock}

    </span>

</td>

Then add to style.css:

/* =========================
   STOCK BADGES
========================= */

.stock-badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: bold;
}

.in-stock {
    background: #dcfce7;
    color: #166534;
}

.out-stock {
    background: #fee2e2;
    color: #991b1b;
}
Step 11.8: Refresh

Save all files.

Then:

Ctrl + Shift + R

Login again if necessary.

You should now have something closer to:

┌─────────────────────────────────────────────────────────┐
│ 💊 Pharmacy FEFO Manager                   Welcome       │
│                                              [Logout]    │
└─────────────────────────────────────────────────────────┘

   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │ 💊           │ │ 📦           │ │ 🚨           │
   │ Medicines    │ │ Stock        │ │ Expiring     │
   │     4        │ │     145      │ │     2        │
   └──────────────┘ └──────────────┘ └──────────────┘


   🚨 Expiry Alerts
   ─────────────────────────────────────────────────────


   💊 Medicines                         [+ Add Medicine]

   🔎 Search...       Sort Name ▼       Ascending ▼

   ┌────────────────────────────────────────────────────┐
   │ Medicine │ Generic │ Manufacturer │ Stock │ Actions│
   ├────────────────────────────────────────────────────┤
   │ Paracetamol       │ ... │ ... │ 🟢 20 │ ...       │
   │ Ibuprofen         │ ... │ ... │ 🟢 40 │ ...       │
   └────────────────────────────────────────────────────┘
Section 11 completion

We're looking for:

✅ Summary cards visible
✅ Search still works
✅ Sorting still works
✅ Medicine table still works
✅ Stock badges visible
✅ Expiry count visible
✅ Add Medicine still works
✅ Batch operations still work
✅ Dispensing still works

Don't worry about making it perfect yet.

Once you've checked the dashboard, tell me "Section 11 done". Then we'll tackle the remaining submission-critical pieces: accurate dashboard statistics, environment configuration, database initialization/seed handling, API error handling, final testing, and the required GitHub documentation files.
One thing to check before calling T1 done

Test this sequence:

Initial stock = 20
Threshold = 10

Dispense 5
→ stock = 15
→ no notification

Dispense 10
→ stock = 5
→ REORDER_ALERT

Dispense 2
→ stock = 3
→ no second alert

And verify:

GET /outbox

contains the reorder event.

Once this works, tell me "T1 done".

Then we'll enter the final submission phase: clean up the project, make the dashboard statistics accurate, add proper error handling, prepare README.md, REASONING.md, .gitignore, and handle AI_LOGS.md correctly for the evaluator.

def dispense_medicine(
    medicine_id: int,
    data: DispenseRequest,
    db: Session = Depends(get_db)
):

    # Check that medicine exists
    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    today = date.today()
    stock_before = sum(
    batch.quantity
    for batch in (
        db.query(Batch)
        .filter(
            Batch.medicine_id == medicine_id,
            Batch.quantity > 0,
            Batch.expiry_date >= today,
            Batch.status == "active"
        )
        .all()
    )
)
    # Get ONLY valid, non-expired batches.
    # Earliest expiry comes first.
    valid_batches = (
        db.query(Batch)
        .filter(
            Batch.medicine_id == medicine_id,
            Batch.quantity > 0,
            Batch.expiry_date >= today,
            Batch.status == "active"
        )
        .order_by(Batch.expiry_date.asc(), Batch.id.asc())
        .all()
    )

    available_stock = sum(
        batch.quantity
        for batch in valid_batches
    )

    # Do not partially dispense if there is
    # not enough valid stock.
    if data.quantity > available_stock:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Insufficient sellable stock",
                "requested": data.quantity,
                "available": available_stock
            }
        )

    remaining = data.quantity
    dispensed_from = []

    # Consume earliest-expiring valid batches first.
    for batch in valid_batches:

        if remaining == 0:
            break

        quantity_taken = min(
            batch.quantity,
            remaining
        )

        batch.quantity -= quantity_taken
        remaining -= quantity_taken

        dispensed_from.append({
            "batch_id": batch.id,
            "batch_number": batch.batch_number,
            "expiry_date": batch.expiry_date,
            "quantity_dispensed": quantity_taken,
            "remaining_in_batch": batch.quantity
        })

        # Calculate remaining sellable stock
remaining_stock = sum(
    batch.quantity
    for batch in (
        db.query(Batch)
        .filter(
            Batch.medicine_id == medicine_id,
            Batch.quantity > 0,
            Batch.expiry_date >= today,
            Batch.status == "active"
        )
        .all()
    )
)


# Send reorder notification when stock
# crosses below the threshold
        if (
    stock_before >= medicine.reorder_threshold
    and remaining_stock < medicine.reorder_threshold
):

    NotificationService.send_reorder_alert(
        db=db,
        medicine=medicine,
        current_stock=remaining_stock
    )


    db.commit()

    # Commit all changes together.

    return {
        "message": "Medicine dispensed successfully",
        "medicine": medicine.name,
        "quantity_dispensed": data.quantity,
        "dispensed_from": dispensed_from
    }

give me updated function

Yes. Your indentation got mixed up around remaining_stock and the notification if. Replace your entire dispense_medicine() function with this clean version:

@router.post("/{medicine_id}/dispense")
def dispense_medicine(
    medicine_id: int,
    data: DispenseRequest,
    db: Session = Depends(get_db)
):
    # Check that medicine exists
    medicine = (
        db.query(Medicine)
        .filter(Medicine.id == medicine_id)
        .first()
    )

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    today = date.today()

    # Calculate sellable stock BEFORE dispensing
    stock_before = sum(
        batch.quantity
        for batch in (
            db.query(Batch)
            .filter(
                Batch.medicine_id == medicine_id,
                Batch.quantity > 0,
                Batch.expiry_date >= today,
                Batch.status == "active"
            )
            .all()
        )
    )

    # Get ONLY valid, non-expired, active batches.
    # Earliest expiry comes first = FEFO
    valid_batches = (
        db.query(Batch)
        .filter(
            Batch.medicine_id == medicine_id,
            Batch.quantity > 0,
            Batch.expiry_date >= today,
            Batch.status == "active"
        )
        .order_by(
            Batch.expiry_date.asc(),
            Batch.id.asc()
        )
        .all()
    )

    # Calculate available sellable stock
    available_stock = sum(
        batch.quantity
        for batch in valid_batches
    )

    # Do not partially dispense if stock is insufficient
    if data.quantity > available_stock:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Insufficient sellable stock",
                "requested": data.quantity,
                "available": available_stock
            }
        )

    remaining = data.quantity
    dispensed_from = []

    # Consume earliest-expiring batches first
    for batch in valid_batches:

        if remaining == 0:
            break

        quantity_taken = min(
            batch.quantity,
            remaining
        )

        batch.quantity -= quantity_taken
        remaining -= quantity_taken

        dispensed_from.append({
            "batch_id": batch.id,
            "batch_number": batch.batch_number,
            "expiry_date": batch.expiry_date,
            "quantity_dispensed": quantity_taken,
            "remaining_in_batch": batch.quantity
        })

    # Calculate remaining sellable stock AFTER dispensing
    remaining_stock = sum(
        batch.quantity
        for batch in (
            db.query(Batch)
            .filter(
                Batch.medicine_id == medicine_id,
                Batch.quantity > 0,
                Batch.expiry_date >= today,
                Batch.status == "active"
            )
            .all()
        )
    )

    # Send reorder notification only when
    # stock crosses from >= threshold to < threshold
    if (
        stock_before >= medicine.reorder_threshold
        and remaining_stock < medicine.reorder_threshold
    ):
        NotificationService.send_reorder_alert(
            db=db,
            medicine=medicine,
            current_stock=remaining_stock
        )

    # Commit all changes together
    db.commit()

    return {
        "message": "Medicine dispensed successfully",
        "medicine": medicine.name,
        "quantity_dispensed": data.quantity,
        "dispensed_from": dispensed_from,
        "stock_before": stock_before,
        "remaining_stock": remaining_stock
    }
Also check this import

At the top of medicine_routes.py, make sure you have:

from .notification_service import NotificationService

Your imports should include:

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import get_db
from .models import Medicine, Batch
from .auth import get_current_user
from .notification_service import NotificationService
Then save and restart
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

This version preserves your FEFO behavior and adds the reorder notification cleanly.

Test it with:

Stock = 20
Threshold = 10

Dispense 5  → Stock = 15 → No alert
Dispense 10 → Stock = 5  → REORDER_ALERT

Then check:

GET /outbox

You should see the notification. 🔔