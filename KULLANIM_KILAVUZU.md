# 📘 İş & Finans Pro — Müşteri Kullanım Kılavuzu

Bu sistem; işletmenizin gelir-gider akışını, müşteri kayıtlarını (CRM) ve yapay zeka destekli finansal analizlerinizi tek bir merkezden güvenle yönetmeniz için tasarlanmıştır.

## 1. Sistemi Başlatma
1. Proje klasörünü açın ve adres çubuğuna `cmd` yazarak komut satırını başlatın.
2. Aşağıdaki komutu yazıp `Enter` tuşuna basın:
   `python -m uvicorn main:app --reload`
3. Tarayıcınızı açın ve adres çubuğuna **`http://127.0.0.1:8000`** yazın.

## 2. Giriş Bilgileri
* **Kullanıcı Adı:** `admin`
* **Şifre:** `123456`

## 3. Temel Özelliklerin Kullanımı
* **Müşteri Ekleme (CRM):** Orta paneldeki "Yeni Müşteri Ekle" formunu kullanarak müşterilerinizin iletişim ve firma bilgilerini kaydedebilirsiniz.
* **Gelir / Gider Kaydı:** Sol panelden işlem türünü (Gelir/Gider), tarihini, tutarını ve ilgili müşteriyi seçerek finansal hareketlerinizi işleyebilirsiniz.
* **PDF Makbuz / Dekont Oluşturma:** Alt tablodaki herhangi bir işlemin sağındaki **🧾 Makbuz** butonuna tıklayarak kurumsal belge görünümünü açabilir ve **"Yazdır / PDF Olarak Kaydet"** butonuyla müşterinize iletebilirsiniz.
* **Excel (CSV) Rapor Alma:** Sağ üst köşedeki **📥 CSV Rapor İndir** butonuna basarak tüm finansal geçmişinizi tek tıkla tablo formatında bilgisayarınıza indirebilirsiniz.
* **Yapay Zeka Finansal Danışman:** `ai_service.py` dosyasına Google AI Studio API anahtarınızı eklediğinizde, sistem verilerinizi analiz ederek size özel tasarruf ve büyüme tavsiyeleri üretir.

## 4. Veri Yedekleme
Tüm verileriniz proje klasöründeki **`finans_pro.db`** dosyasında güvenle saklanır. Haftalık olarak bu dosyanın bir kopyasını harici bir diske veya buluta kopyalayarak yedek alabilirsiniz.
