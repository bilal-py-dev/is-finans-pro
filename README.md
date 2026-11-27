# 🚀 İş & Finans Pro — Yapay Zeka Destekli CRM ve Finans Yönetim Paneli

Modern işletmeler, ajanslar ve freelancer'lar için geliştirilmiş; **FastAPI**, **SQLite** ve **Google Gemini AI** tabanlı kurumsal müşteri ve finans yönetim platformu.

## ✨ Öne Çıkan Özellikler
- **Güvenli Oturum Yönetimi:** SHA-256 şifreleme ve Session tabanlı yönetici girişi.
- **CRM & Finans Entegrasyonu:** Müşteri bazlı gelir-gider takibi, canlı kâr marjı hesaplama ve görsel dağılım grafiği.
- **Gemini AI Finansal Danışman:** İşletme nakit akışını analiz ederek büyüme ve maliyet optimizasyonu önerileri sunan yapay zeka motoru.
- **Tek Tıkla PDF Makbuz & CSV Raporlama:** Harici ofis yazılımlarına ihtiyaç duymadan Excel uyumlu CSV dışa aktarım ve yazdırılabilir kurumsal makbuz oluşturma.
- **Bağımsız & Hızlı Arayüz:** Harici CDN bağımlılığı olmayan, sıfır gecikmeli karanlık mod (Dark UI) tasarım.

## 🛠️ Kullanılan Teknolojiler
- **Backend:** Python 3, FastAPI, Uvicorn, Jinja2
- **Veritabanı:** SQLite3
- **Yapay Zeka:** Google GenAI SDK (Gemini 2.5 Flash)
- **Arayüz:** Semantic HTML5, Modern Responsive CSS3

## ⚡ Hızlı Kurulum
```bash
pip install -r requirements.txt
python seed_data.py
python -m uvicorn main:app --reload
```
