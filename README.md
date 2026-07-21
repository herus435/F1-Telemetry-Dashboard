# 🏎️ F1 Telemetry Dashboard

FastAPI ve Streamlit kullanılarak geliştirilmiş, Formula 1 araç telemetrilerini dinamik olarak çeken ve görselleştiren Full-Stack web uygulaması. FastF1 kütüphanesinin güncel veri mimarisi baz alınarak tasarlanmıştır.

## Özellikler
* **Canlı Veri Çekimi:** F1 API'sinden seçilen pilotun en hızlı tur ve araç telemetri verileri.
* **Performanslı Mimari:** In-memory caching (@lru_cache) sistemiyle optimize edilmiş milisaniyelik API yanıt süresi.
* **İnteraktif Arayüz:** Streamlit tabanlı dinamik ve kullanıcı dostu hız grafikleri.

## Kurulum
Projeyi yerel bilgisayarınızda çalıştırmak için:

1. Repoyu klonlayın: `git clone https://github.com/herus435/F1-Telemetry-Dashboard.git`
2. Kütüphaneleri kurun: `pip install fastapi uvicorn streamlit fastf1 pandas`
3. Backend'i başlatın: `uvicorn main:app --reload`
4. Frontend'i başlatın: `streamlit run frontend.py`
