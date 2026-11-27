from database import get_connection, init_db
from datetime import datetime, timedelta

def load_sample_data():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    # Örnek Müşteriler
    sample_clients = [
        ("Ahmet Yılmaz", "Yılmaz E-Ticaret A.Ş.", "ahmet@yilmazeticaret.com", "0532 555 0101"),
        ("Zeynep Kaya", "Kaya Dijital Ajans", "zeynep@kayadijital.com", "0541 555 0202"),
        ("Mehmet Demir", "Demir Lojistik Ltd.", "m.demir@demirlojistik.com", "0505 555 0303"),
        ("Elif Arslan", "Nova Teknoloji Girişimi", "elif@novatech.io", "0554 555 0404")
    ]

    today = datetime.now().strftime("%Y-%m-%d")
    client_ids = []

    for name, company, email, phone in sample_clients:
        cursor.execute(
            "INSERT INTO clients (name, company, email, phone, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, company, email, phone, today)
        )
        client_ids.append(cursor.lastrowid)

    # Örnek Gelir ve Gider Hareketleri
    d1 = (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d")
    d2 = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")
    d3 = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")
    d4 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    sample_transactions = [
        (client_ids[0], "Gelir", "Özel CRM & Stok Yazılımı", 28500.00, "Anahtar teslim web paneli ve veritabanı kurulumu", d1),
        (client_ids[1], "Gelir", "Otomasyon & Bot Geliştirme", 14000.00, "Müşteri bildirim ve veri çekme otomasyonu", d2),
        (None, "Gider", "Bulut Sunucu & Hosting", 1850.00, "Yıllık VDS ve alan adı yenileme gideri", d2),
        (client_ids[2], "Gelir", "Veri Analiz Raporlama Modülü", 19500.00, "Excel/CSV entegrasyonlu finans takip sistemi", d3),
        (None, "Gider", "API & Yazılım Lisansları", 950.00, "Aylık yapay zeka API ve geliştirici araçları", d3),
        (client_ids[3], "Gelir", "API Entegrasyonu & Danışmanlık", 11000.00, "Ödeme sistemi ve webhook bağlantıları", d4),
        (None, "Gider", "Ofis & Ekipman Gideri", 3200.00, "Donanım ve çalışma ortamı iyileştirmesi", today)
    ]

    for cid, t_type, category, amount, desc, date in sample_transactions:
        cursor.execute(
            "INSERT INTO transactions (client_id, type, category, amount, description, date) VALUES (?, ?, ?, ?, ?, ?)",
            (cid, t_type, category, amount, desc, date)
        )

    conn.commit()
    conn.close()
    print("✅ 4 örnek müşteri ve 7 finansal işlem başarıyla yüklendi!")

if __name__ == "__main__":
    load_sample_data()
