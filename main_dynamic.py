import os
from fastapi import FastAPI
import fastf1
from functools import lru_cache

app = FastAPI(title="F1 Telemetri Servisi (Tam Dinamik)")

# Önbellek klasörü kontrolü
if not os.path.exists('cache_verileri'):
    os.makedirs('cache_verileri')
fastf1.Cache.enable_cache('cache_verileri')

@lru_cache(maxsize=32)
def fetch_and_process_telemetry(year: int, event: str, driver: str):
    session = fastf1.get_session(year, event, 'R')
    session.load(weather=False, messages=False)
    
    lap = session.laps.pick_drivers(driver).pick_fastest()
    car_data = lap.get_car_data().add_distance()
    
    return {
        "distance": car_data['Distance'].tolist()[::10],
        "speed": car_data['Speed'].tolist()[::10],
        "gear": car_data['nGear'].tolist()[::10]
    }

@app.get("/api/telemetry")
def get_telemetry_data(year: int = 2023, event: str = 'Zandvoort', driver: str = 'VER'):
    telemetry = fetch_and_process_telemetry(year, event, driver)
    
    return {
        "driver": driver,
        "event": event,
        "year": year,
        "telemetry": telemetry
    }