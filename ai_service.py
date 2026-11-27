import os
from google import genai

# Google AI Studio'dan aldığın API anahtarını buraya yapıştırabilirsin
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "BURAYA_API_ANAHTARINI_YAZ")

def analyze_finances(total_income: float, total_expense: float, client_count: int, recent_transactions: list) -> str:
    net_profit = total_income - total_expense
    profit_margin = (net_profit / total_income * 100) if total_income > 0 else 0

    # Eğer henüz geçerli bir API anahtarı girilmediyse sistemin çalışmaya devam etmesi için yerel akıllı özet:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "BURAYA_API_ANAHTARINI_YAZ":
        if total_income == 0 and total_expense == 0:
            return "Henüz finansal veri girilmemiş. İlk gelir ve gider kayıtlarını eklediğinde yapay zeka danışmanın kâr marjını ve büyüme fırsatlarını analiz etmeye başlayacak."
        
        status_msg = "Kârlı bir dönemdesiniz." if net_profit > 0 else "Giderleriniz gelirlerinizi aşmış durumda, acil nakit akışı planlaması önerilir."
        return (
            f"📊 Hızlı Finansal Özet: Net kârınız {net_profit:,.2f} TL (Kâr Marjı: %{profit_margin:.1f}). {status_msg} "
            f"Aktif {client_count} müşteriniz bulunuyor. (Detaylı Gemini AI stratejileri için ai_service.py dosyasına API anahtarınızı ekleyin.)"
        )

    # Gerçek Gemini AI Analizi
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        tx_summary = "\n".join([f"- {t['date']}: {t['type']} | {t['category']} | {t['amount']} TL ({t['description']})" for t in recent_transactions[:10]])
        
        prompt = f"""
        Sen kıdemli bir finansal danışman ve iş geliştirme uzmanısın. Aşağıdaki işletme verilerini analiz et ve işletme sahibine 3 maddelik kısa, net, uygulanabilir büyüme ve tasarruf tavsiyesi ver (Türkçe, profesyonel ton):
        
        - Toplam Gelir: {total_income:,.2f} TL
        - Toplam Gider: {total_expense:,.2f} TL
        - Net Kâr: {net_profit:,.2f} TL (Kâr Marjı: %{profit_margin:.1f})
        - Toplam Müşteri Sayısı: {client_count}
        - Son İşlemler:
        {tx_summary}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"AI Analizi şu an oluşturulamadı (Bağlantı/Anahtar kontrolü gerekli). Mevcut Net Kâr: {net_profit:,.2f} TL."
