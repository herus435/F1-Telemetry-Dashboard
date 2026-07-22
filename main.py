import os
from fastapi import FastAPI
import fastf1
from functools import lru_cache

app = FastAPI(title="F1 Telemetri Servisi")

# Klasör sistemde yoksa otomatik olarak oluşturuyoruz
if not os.path.exists('cache_verileri'):
    os.makedirs('cache_verileri')

fastf1.Cache.enable_cache('cache_verileri')

@lru_cache(maxsize=32)
def fetch_and_process_telemetry(year: int, event: str, driver: str):
    session = fastf1.get_session(year, event, 'R')
    # Performanslı yükleme standartları
    session.load(weather=False, messages=False)
    
    lap = session.laps.pick_drivers(driver).pick_fastest()
    car_data = lap.get_car_data().add_distance()
    
    distances = car_data['Distance'].tolist()[::10]
    speeds = car_data['Speed'].tolist()[::10]
    gears = car_data['nGear'].tolist()[::10]
    
    return {
        "distance": distances,
        "speed": speeds,
        "gear": gears
    }

# İşte demin eksik olan asıl uç noktamız:
@app.get("/api/telemetry")
def get_telemetry_data(year: int = 2023, event: str = 'Zandvoort', driver: str = 'VER'):
    telemetry = fetch_and_process_telemetry(year, event, driver)
    
    return {
        "driver": driver,
        "event": event,
        "year": year,
        "telemetry": telemetry
    }
