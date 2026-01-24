import google.generativeai as genai
import streamlit as st

# Streamlit secrets içindeki key'i alıyoruz
# Eğer lokalde çalışıyorsan buraya direkt api_key="AIza..." yazabilirsin.
try:
    api_key = st.secrets["GOOGLE_API_KEYS"][0] # Secrets listesinden ilkini dener
except:
    api_key = input("API Key'inizi yapıştırın: ")

genai.configure(api_key=api_key)

print("\n--- ERİŞİLEBİLİR MODELLERİN LİSTESİ ---")
try:
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            count += 1
    
    if count == 0:
        print("HATA: Hiçbir modele erişim izni görünmüyor. API Key veya faturalandırma ayarlarını kontrol et.")
    else:
        print(f"\nToplam {count} model bulundu.")
        print("Tavsiye: Listede 'gemini-2.0', 'gemini-1.5-pro' veya 'exp' geçen en yeni versiyonu seçmelisin.")

except Exception as e:
    print("Hata oluştu:", e)