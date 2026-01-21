import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Key Tester Stable", page_icon="🛡️", layout="wide")

st.title("🛡️ Tutarlı API Key Test Cihazı")
st.info("Bu sürüm 'Yalancı Hata' vermemek için her anahtarı 2 kez kontrol eder ve aralarda bekler. Biraz yavaş çalışır ama sonuçlar kesindir.")

# --- FONKSİYON: ANAHTARI ÇİFT KONTROL ET ---
def test_key_stable(api_key):
    # Denenecek Modeller (En garantiden en yeniye)
    # Not: 2.5 Flash şu an en popüler çalışan model
    models_to_try = [
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-1.5-pro',
        'gemini-pro'
    ]

    def try_connect():
        """Tek seferlik bağlantı denemesi"""
        try:
            genai.configure(api_key=api_key)
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    model.generate_content("Test", request_options={"timeout": 5})
                    return True, model_name, "✅ Sorunsuz"
                except:
                    continue
            
            # Listeden bulma (Son çare)
            available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available:
                m_name = available[0].replace("models/", "")
                genai.GenerativeModel(m_name).generate_content("T")
                return True, m_name, "⚠️ Listeden"
                
            return False, None, "Erişim Yok"
        except Exception as e:
            return False, None, str(e)

    # --- 1. DENEME ---
    success, model, msg = try_connect()
    if success:
        return success, model, msg
    
    # --- 2. DENEME (Eğer ilkinde hata verdiyse) ---
    # Belki sadece hız sınırına takılmıştır, 2 saniye bekle tekrar dene
    time.sleep(2) 
    success_retry, model_retry, msg_retry = try_connect()
    
    if success_retry:
        return True, model_retry, "✅ İkinci denemede açıldı"
    
    return False, None, "❌ Tamamen Kapalı (Veya Kota Dolu)"

# --- ARAYÜZ ---
raw_keys = st.text_area("Anahtarları Buraya Yapıştır:", height=300)

if st.button("Güvenli Taramayı Başlat 🛡️"):
    if not raw_keys:
        st.error("Anahtar yok.")
    else:
        keys_list = [k.strip() for k in raw_keys.split('\n') if k.strip()]
        
        st.write(f"🕵️‍♂️ **{len(keys_list)}** anahtar titizlikle taranıyor... (Biraz sürebilir)")
        progress_bar = st.progress(0)
        
        working_keys = []
        
        col1, col2, col3 = st.columns([3, 1, 2])
        col1.markdown("**Anahtar**")
        col2.markdown("**Durum**")
        col3.markdown("**Model**")
        st.divider()
        
        for i, api_key in enumerate(keys_list):
            progress_bar.progress((i + 1) / len(keys_list))
            
            # Testi Yap
            is_working, model_name, status_msg = test_key_stable(api_key)
            
            c1, c2, c3 = st.columns([3, 1, 2])
            masked_key = f"...{api_key[-8:]}" if len(api_key) > 8 else api_key
            c1.code(masked_key)
            
            if is_working:
                c2.success("AKTİF")
                c3.info(f"`{model_name}`")
                working_keys.append(api_key)
            else:
                c2.error("PASİF")
                c3.caption("⛔ Erişim Yok")
            
            # HIZ SINIRINA TAKILMAMAK İÇİN BEKLEME (ÖNEMLİ)
            time.sleep(1.0) 
            
        st.success("Tarama Tamamlandı!")
        
        if working_keys:
            st.subheader("💎 Sağlam Liste")
            formatted_keys = 'GOOGLE_API_KEYS = [\n' + ',\n'.join([f'    "{k}"' for k in working_keys]) + '\n]'
            st.code(formatted_keys, language="toml")
        else:
            st.error("Çalışan anahtar yok.")