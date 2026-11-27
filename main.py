from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
import csv
import io
import math
import os
from pathlib import Path

from database import get_connection, hash_password, init_db
from ai_service import analyze_finances

app = FastAPI(title="İş & Finans Pro SaaS")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "gelistirme-icin-yedek-anahtar-degistirin")
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
init_db()

def get_current_user(request: Request):
    return request.session.get("user")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})

@app.post("/login")
async def login_action(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password))
    ).fetchone()
    conn.close()

    if user:
        request.session["user"] = {"id": user["id"], "username": user["username"], "company": user["company_name"]}
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse(request=request, name="login.html", context={"error": "Kullanıcı adı veya şifre hatalı!"})

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    conn = get_connection()
    clients = conn.execute("SELECT * FROM clients ORDER BY id DESC").fetchall()
    transactions = conn.execute("""
        SELECT t.*, c.name as client_name 
        FROM transactions t 
        LEFT JOIN clients c ON t.client_id = c.id 
        ORDER BY t.date DESC, t.id DESC
    """).fetchall()

    total_income = sum(t["amount"] for t in transactions if t["type"] == "Gelir")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "Gider")
    net_profit = total_income - total_expense

    ai_advice = analyze_finances(total_income, total_expense, len(clients), [dict(t) for t in transactions])
    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "clients": clients,
            "transactions": transactions,
            "total_income": total_income,
            "total_expense": total_expense,
            "net_profit": net_profit,
            "ai_advice": ai_advice,
            "today": datetime.now().strftime("%Y-%m-%d")
        }
    )

@app.post("/add-client")
async def add_client(request: Request, name: str = Form(...), company: str = Form(""), email: str = Form(""), phone: str = Form("")):
    if not get_current_user(request):
        return RedirectResponse(url="/login", status_code=303)

    conn = get_connection()
    conn.execute(
        "INSERT INTO clients (name, company, email, phone, created_at) VALUES (?, ?, ?, ?, ?)",
        (name, company, email, phone, datetime.now().strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/add-transaction")
async def add_transaction(
    request: Request,
    type: str = Form(...),
    category: str = Form(...),
    amount: float = Form(...),
    client_id: str = Form(""),
    description: str = Form(""),
    date: str = Form(...)
):
    if not get_current_user(request):
        return RedirectResponse(url="/login", status_code=303)

    if type not in {"Gelir", "Gider"}:
        return RedirectResponse(url="/", status_code=303)
    if not math.isfinite(amount) or amount <= 0:
        return RedirectResponse(url="/", status_code=303)

    try:
        cid = int(client_id) if client_id.strip() else None
    except ValueError:
        return RedirectResponse(url="/", status_code=303)
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return RedirectResponse(url="/", status_code=303)

    conn = get_connection()
    if cid is not None:
        if not conn.execute("SELECT 1 FROM clients WHERE id = ?", (cid,)).fetchone():
            conn.close()
            return RedirectResponse(url="/", status_code=303)
    conn.execute(
        "INSERT INTO transactions (client_id, type, category, amount, description, date) VALUES (?, ?, ?, ?, ?, ?)",
        (cid, type, category, amount, description, date)
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

# İşlem Silme Rotası
@app.post("/delete-transaction/{tx_id}")
async def delete_transaction(request: Request, tx_id: int):
    if not get_current_user(request):
        return RedirectResponse(url="/login", status_code=303)

    conn = get_connection()
    conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

# YENİ: Yazdırılabilir / PDF Makbuz & Teklif Belgesi Rotası
@app.get("/receipt/{tx_id}", response_class=HTMLResponse)
async def view_receipt(request: Request, tx_id: int):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    conn = get_connection()
    tx = conn.execute("""
        SELECT t.*, c.name as client_name, c.company as client_company, c.email as client_email, c.phone as client_phone
        FROM transactions t
        LEFT JOIN clients c ON t.client_id = c.id
        WHERE t.id = ?
    """, (tx_id,)).fetchone()
    conn.close()

    if not tx:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(request=request, name="receipt.html", context={"user": user, "tx": tx})

@app.get("/export-csv")
async def export_csv(request: Request):
    if not get_current_user(request):
        return RedirectResponse(url="/login", status_code=303)

    conn = get_connection()
    transactions = conn.execute("""
        SELECT t.date, t.type, t.category, c.name as client_name, t.amount, t.description 
        FROM transactions t 
        LEFT JOIN clients c ON t.client_id = c.id 
        ORDER BY t.date DESC
    """).fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["Tarih", "Islem Turu", "Kategori", "Musteri", "Tutar (TL)", "Aciklama"])
    
    for t in transactions:
        writer.writerow([t["date"], t["type"], t["category"], t["client_name"] or "-", t["amount"], t["description"]])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue().encode("utf-8-sig")]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=finansal_rapor.csv"}
    )
