import fastf1
import json
import os

# Cache'i aktif ediyoruz
fastf1.Cache.enable_cache('cache_verileri')

# Oturumu yüklüyoruz
session = fastf1.get_session(2023, 'Zandvoort', 'R')
session.load(weather=False, messages=False)

# Arayüzdeki pilotlar için verileri toplayacağımız sözlük
drivers = ["VER", "ALO", "HAM", "LEC", "SAI", "NOR"]
telemetry_db = {}

print("Veriler işleniyor, lütfen bekleyin...")

for driver in drivers:
    lap = session.laps.pick_drivers(driver).pick_fastest()
    car_data = lap.get_car_data().add_distance()
    
    # Sadece arayüzün ihtiyacı olan hafif listeleri alıyoruz
    telemetry_db[driver] = {
        "distance": car_data['Distance'].tolist()[::10],
        "speed": car_data['Speed'].tolist()[::10],
        "gear": car_data['nGear'].tolist()[::10]
    }
    print(f"{driver} verisi hazırlandı.")

# Verileri ufak bir JSON dosyasına kaydediyoruz(Ortalama 100-200 KB)
with open('telemetry_db.json', 'w') as f:
    json.dump(telemetry_db, f)
    
print("İşlem tamam! telemetry_db.json dosyası oluşturuldu.")