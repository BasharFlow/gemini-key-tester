import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Key Tester Turbo", page_icon="⚡", layout="wide")

st.title("⚡ Hızlandırılmış Key Test Cihazı")
st.info("Bu sürüm 1.5 Flash'ı atlar. Doğrudan 2.0 ve Pro modellerini dener.")

# --- FONKSİYON: SADECE İŞE YARAYANLARI TEST ET ---
def test_key_turbo(api_key):
    try:
        genai.configure(api_key=api_key)
        
        # LİSTE GÜNCELLENDİ: Vakit kaybettiren 1.5 Flash çıkarıldı.
        models_to_try = [
            'gemini-2.0-flash',      # En yeni ve hızlı
            'gemini-2.0-flash-exp',  # Deneysel (Genelde açıktır)
            'gemini-1.5-pro',        # Flash yoksa Pro vardır
            'gemini-pro'             # En eski (Çoğu eski projede bu açıktır)
        ]
        
        # 1. Aşama: Hızlı Liste Kontrolü
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # Ufak bir "Test" atışı
                model.generate_content("Test", request_options={"timeout": 4})
                return True, model_name, "✅ Sorunsuz"
            except Exception:
                continue # Bu model olmadı, sonrakine geç
        
        # 2. Aşama: Hiçbiri olmadıysa, son çare hesaptaki açık listeye bak
        # (Belki çok garip bir model ismi vardır, onu bulalım)
        try:
            available_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
            
            if available_models:
                # Listeden 'flash' olmayan ama 'pro' olan bir şey bulmaya çalış
                first_model = available_models[0].replace("models/", "")
                model = genai.GenerativeModel(first_model)
                model.generate_content("Test", request_options={"timeout": 4})
                return True, first_model, "⚠️ Listeden Bulundu"
        except:
            pass
                
        return False, None, "❌ Modeller Kapalı veya Kota Dolu"

    except Exception as e:
        return False, None, f"❌ Geçersiz Anahtar"

# --- ARAYÜZ ---
raw_keys = st.text_area("Anahtarları Buraya Yapıştır (Her satıra bir tane):", height=300)

if st.button("Hızlı Taramayı Başlat 🚀"):
    if not raw_keys:
        st.error("Lütfen anahtar yapıştırın.")
    else:
        # Anahtarları temizle
        keys_list = [k.strip() for k in raw_keys.split('\n') if k.strip()]
        
        st.write(f"🚀 **{len(keys_list)}** anahtar hızla taranıyor...")
        progress_bar = st.progress(0)
        
        working_keys = []
        
        col1, col2, col3 = st.columns([3, 1, 2])
        col1.markdown("**Anahtar**")
        col2.markdown("**Durum**")
        col3.markdown("**Çalışan Model**")
        st.write("---")
        
        for i, api_key in enumerate(keys_list):
            progress_bar.progress((i + 1) / len(keys_list))
            
            # Testi Yap
            is_working, model_name, status_msg = test_key_turbo(api_key)
            
            c1, c2, c3 = st.columns([3, 1, 2])
            masked_key = f"...{api_key[-8:]}" if len(api_key) > 8 else api_key
            c1.code(masked_key)
            
            if is_working:
                c2.success("AKTİF")
                c3.info(f"`{model_name}`")
                working_keys.append(api_key)
            else:
                c2.error("PASİF")
                c3.caption(status_msg)
            
            # Çok hızlı olmasın, Google banlamasın (0.2sn ideal)
            time.sleep(0.2)
            
        st.success("Tarama Bitti!")
        
        if working_keys:
            st.subheader("💎 Kopyalamaya Hazır Liste")
            formatted_keys = 'GOOGLE_API_KEYS = [\n' + ',\n'.join([f'    "{k}"' for k in working_keys]) + '\n]'
            st.code(formatted_keys, language="toml")
        else:
            st.error("Çalışan anahtar bulunamadı.")