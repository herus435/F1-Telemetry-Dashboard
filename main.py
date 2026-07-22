from fastapi import FastAPI
import json

app = FastAPI(title="F1 Telemetri Servisi (Ultra Hafif Sürüm)")

# Sunucu başlarken önceden hazırladığımız ufak veriyi RAM'e alıyoruz
with open('telemetry_db.json', 'r') as f:
    PRELOADED_DATA = json.load(f)

@app.get("/api/telemetry")
def get_telemetry_data(year: int = 2023, event: str = 'Zandvoort', driver: str = 'VER'):
    # Veri kütüphaneden hesaplanmıyor, doğrudan JSON dosyamızdan milisaniyeler içinde çekiliyor
    if driver in PRELOADED_DATA:
        return {
            "driver": driver,
            "event": event,
            "year": year,
            "telemetry": PRELOADED_DATA[driver]
        }
    return {"error": "Bu pilot için veri bulunamadı."}