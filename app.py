from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3
import os

app = FastAPI()

# Set up static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database setup
DATABASE = 'database.db'

# Ensure the database and tables are created
if not os.path.exists(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE UserProfile (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        email TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE SmartContract (
                        contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        performance_metrics TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE Transaction (
                        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        amount REAL NOT NULL,
                        timestamp TEXT NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES UserProfile(user_id)
                    )''')
    cursor.execute('''CREATE TABLE MarketTrend (
                        trend_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        data_points TEXT NOT NULL
                    )''')
    # Insert demo data
    cursor.execute("INSERT INTO UserProfile (username, email, created_at) VALUES (?, ?, ?)",
                   ("demo_user", "demo@example.com", datetime.now().isoformat()))
    cursor.execute("INSERT INTO SmartContract (name, performance_metrics) VALUES (?, ?)",
                   ("Demo Contract", "{'metric1': 100, 'metric2': 200}"))
    cursor.execute("INSERT INTO Transaction (user_id, amount, timestamp) VALUES (?, ?, ?)",
                   (1, 150.75, datetime.now().isoformat()))
    cursor.execute("INSERT INTO MarketTrend (name, data_points) VALUES (?, ?)",
                   ("Demo Trend", "[{'time': '2023-01-01', 'value': 100}, {'time': '2023-01-02', 'value': 110}]")
                   )
    conn.commit()
    conn.close()

# Data models
class UserProfile(BaseModel):
    user_id: int
    username: str
    email: str
    created_at: datetime

class SmartContract(BaseModel):
    contract_id: int
    name: str
    performance_metrics: dict

class Transaction(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    timestamp: datetime

class MarketTrend(BaseModel):
    trend_id: int
    name: str
    data_points: List[dict]

# API Endpoints
@app.get("/api/users", response_model=List[UserProfile])
async def get_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM UserProfile")
    users = cursor.fetchall()
    conn.close()
    return [UserProfile(user_id=row[0], username=row[1], email=row[2], created_at=row[3]) for row in users]

@app.post("/api/users", response_model=UserProfile)
async def create_user(user: UserProfile):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO UserProfile (username, email, created_at) VALUES (?, ?, ?)",
                   (user.username, user.email, datetime.now().isoformat()))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return {"user_id": user_id, **user.dict()}

@app.get("/api/contracts", response_model=List[SmartContract])
async def get_contracts():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SmartContract")
    contracts = cursor.fetchall()
    conn.close()
    return [SmartContract(contract_id=row[0], name=row[1], performance_metrics=eval(row[2])) for row in contracts]

@app.get("/api/transactions", response_model=List[Transaction])
async def get_transactions():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transaction")
    transactions = cursor.fetchall()
    conn.close()
    return [Transaction(transaction_id=row[0], user_id=row[1], amount=row[2], timestamp=row[3]) for row in transactions]

@app.get("/api/market-trends", response_model=List[MarketTrend])
async def get_market_trends():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MarketTrend")
    trends = cursor.fetchall()
    conn.close()
    return [MarketTrend(trend_id=row[0], name=row[1], data_points=eval(row[2])) for row in trends]

# HTML Endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root(request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def read_profile(request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/analytics", response_class=HTMLResponse)
async def read_analytics(request):
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/transactions", response_class=HTMLResponse)
async def read_transactions(request):
    return templates.TemplateResponse("transactions.html", {"request": request})

@app.get("/market-trends", response_class=HTMLResponse)
async def read_market_trends(request):
    return templates.TemplateResponse("market_trends.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
