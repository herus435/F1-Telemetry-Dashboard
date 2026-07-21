import os
from fastapi import FastAPI
import fastf1
from functools import lru_cache 

app = FastAPI(title="F1 Telemetri Servisi")

# Klasör sistemde yoksa otomatik olarak oluşturuyoruz
if not os.path.exists('cache_verileri'):
    os.makedirs('cache_verileri')

# Artık klasörün var olduğundan emin olduğumuz için önbelleği güvenle açabiliriz
fastf1.Cache.enable_cache('cache_verileri')

# Bu dekoratör, fonksiyonun son 32 farklı parametre kombinasyonunu RAM'de tutar (Hash'ler)
@lru_cache(maxsize=32)
def fetch_and_process_telemetry(year: int, event: str, driver: str):
    session = fastf1.get_session(year, event, 'R')
    
    # Rapor standartlarına uygun performanslı yükleme[cite: 1]
    session.load(weather=False, messages=False)
    lap = session.laps.pick_drivers(driver).pick_fastest()
    
    # Rapor standartlarına uygun araç verisi çekimi[cite: 1]
    car_data = lap.get_car_data().add_distance()
    
    # Veriyi listelere çevir
    distances = car_data['Distance'].tolist()[::10]
    speeds = car_data['Speed'].tolist()[::10]
    gears = car_data['nGear'].tolist()[::10]
    
    # Sadece işlenmiş ham listeleri döndürüyoruz
    return {
        "distance": distances,
        "speed": speeds,
        "gear": gears
    }


@app.get("/api/telemetry")
def get_telemetry_data(year: int = 2023, event: str = 'Zandvoort', driver: str = 'VER'):
    # Kullanıcıdan istek geldiğinde API bu satıra girer.
    # Eğer bu pilotun verisi daha önce çekilmişse, üstteki fonksiyon HİÇ ÇALIŞTIRILMAZ.
    # Veri doğrudan RAM'den milisaniyeler içinde çekilip 'telemetry' değişkenine atanır.
    telemetry = fetch_and_process_telemetry(year, event, driver)
    
    return {
        "driver": driver,
        "event": event,
        "year": year,
        "telemetry": telemetry
    }
