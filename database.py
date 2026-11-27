import sqlite3
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_NAME = str(BASE_DIR / "finans_pro.db")

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Yöneticiler Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        company_name TEXT DEFAULT 'Yönetim Paneli'
    )
    """)

    # 2. Müşteriler (CRM) Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        company TEXT,
        email TEXT,
        phone TEXT,
        status TEXT DEFAULT 'Aktif',
        created_at TEXT
    )
    """)

    # 3. Finansal İşlemler (Gelir / Gider) Tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    """)

    # Varsayılan Yönetici Hesabı (admin / 123456)
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, password_hash, company_name) VALUES (?, ?, ?)",
            ("admin", hash_password("123456"), "Kurumsal Finans & CRM")
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("✅ Veritabanı ve tablolar başarıyla oluşturuldu!")
