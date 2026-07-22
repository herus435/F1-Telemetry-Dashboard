# 🏎️ F1 Telemetry Dashboard

FastAPI (Backend) ve Streamlit (Frontend) kullanılarak geliştirilmiş, Formula 1 araçlarının tur verilerini ve hız telemetrilerini görselleştiren Full-Stack web uygulaması.

Bu proje, F1 telemetri verilerinin devasa boyutları ve bulut sunucularının (PaaS) bellek kısıtlamaları göz önüne alınarak iki farklı mimariyle tasarlanmıştır:
1. **Cloud/Lite Versiyon:** Düşük RAM (512 MB) ortamları için önceden hesaplanmış (pre-computed) JSON kullanan ETL mimarisi.
2. **Local/Dynamic Versiyon:** Yüksek donanımlı yerel sistemlerde `fastf1` kütüphanesiyle API üzerinden anlık, tam dinamik veri çeken versiyon (`main_dynamic.py`).


---

## 🛠️ Mimari Kararlar ve Trade-off (Ödünleşim)

F1 telemetri verileri yüksek frekanslı GPS kanalları içerdiğinden, tek bir yarış seansının Pandas ile işlenmesi 300-400 MB RAM tüketmektedir. Ücretsiz bulut servislerinde (Render) yaşanan "Out of Memory" (OOM) hatalarını önlemek adına, veriler yerel ortamda çekilip küçültülmüş bir JSON dosyasına (`telemetry_db.json`) dönüştürülmüş ve canlı sunucuya sadece bu hafifletilmiş veriyi okuma görevi verilmiştir.

Projeyi kendi bilgisayarında tüm limitleri kaldırarak anlık veri çekecek şekilde çalıştırmak isteyen geliştiriciler için **Yerel (Dinamik) Kurulum** adımları aşağıya eklenmiştir.

---

## 💻 Yerel Kurulum (Tam Dinamik Versiyon)

Projeyi kendi bilgisayarınızda tüm pilot, yarış ve yıl kombinasyonlarını anlık olarak hesaplayacak şekilde çalıştırmak için repoda halihazırda bulunan `main_dynamic.py` dosyasını kullanabilirsiniz.

### 1. Repoyu Klonlayın ve Gereksinimleri Kurun
Projeyi bilgisayarınıza indirdikten sonra gerekli kütüphaneleri yükleyin:


git clone [https://github.com/herus435/F1-Telemetry-Dashboard.git](https://github.com/herus435/F1-Telemetry-Dashboard.git)
cd F1-Telemetry-Dashboard
pip install -r requirements.txt

### 2. Frontend URL'sini Güncelleyin
`frontend.py` dosyasını açın ve `API_URL` adresini yerel sunucunuzu işaret edecek şekilde değiştirin:


API_URL = "[http://127.0.0.1:8000](http://127.0.0.1:8000)"
### 3. Uygulamayı Başlatın
Terminalinizde iki farklı sekme açın:

Sekme 1 (Backend - FastAPI):
Tam dinamik versiyonu başlatan main_dynamic.py dosyasını çalıştırın.

uvicorn main_dynamic:app --reload


Sekme 2 (Frontend - Streamlit):

streamlit run frontend.py
Artık tarayıcınız üzerinden açılan arayüzde, kendi bilgisayarınızın donanım gücünü kullanarak F1 telemetri verilerini anlık ve eksiksiz bir şekilde çekebilirsiniz!
