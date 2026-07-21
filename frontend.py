import streamlit as st
import requests
import pandas as pd

# Sayfa ayarları
st.set_page_config(page_title="F1 Telemetri Paneli", layout="wide")

st.title("🏎️ Formula 1 Telemetri Analiz Arayüzü")
st.write("Bu arayüz, yerel bilgisayarda çalışan FastAPI sunucusundan canlı veri çekmektedir.")

# Kullanıcıdan pilot seçimi alıyoruz
driver = st.selectbox("Analiz etmek istediğiniz pilotu seçin:", ["VER", "ALO", "HAM", "LEC", "SAI", "NOR"])

# Butona basıldığında çalışacak kısım
if st.button("Telemetriyi Getir"):
    with st.spinner(f"{driver} için veriler API'den çekiliyor..."):
        
        # 1. Kendi Backend'imize HTTP GET isteği atıyoruz
        url = f"http://127.0.0.1:8000/api/telemetry?driver={driver}"
        
        try:
            response = requests.get(url)
            
            # Eğer API'den başarılı (200 OK) yanıt geldiyse
            if response.status_code == 200:
                data = response.json()
                telemetry = data["telemetry"]
                
                # Gelen JSON verisini Pandas DataFrame'e (tabloya) çeviriyoruz
                df = pd.DataFrame({
                    "Mesafe": telemetry["distance"],
                    "Hız": telemetry["speed"],
                    "Vites": telemetry["gear"]
                })
                
                st.success(f"{driver} - Zandvoort 2023 verileri başarıyla yüklendi!")
                
                # 2. Hızlı Metrikler
                col1, col2 = st.columns(2)
                col1.metric("Maksimum Hız", f"{int(df['Hız'].max())} km/s")
                col2.metric("Toplam Veri Noktası", len(df))
                
                # 3. Streamlit'in kendi çizim aracıyla Hız Grafiği
                st.subheader("Hız Profili (Mesafe bazlı)")
                # X ekseni Mesafe, Y ekseni Hız olacak şekilde grafiği ekrana basıyoruz
                st.line_chart(df, x="Mesafe", y="Hız", color="#E10600")
                
            else:
                st.error("API'den veri alınamadı. Hata Kodu: " + str(response.status_code))
                
        except requests.exceptions.ConnectionError:
            st.error("API'ye ulaşılamadı. Lütfen 'uvicorn main:app' komutuyla FastAPI sunucusunun çalıştığından emin ol.")