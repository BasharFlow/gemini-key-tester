import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Key Tester", page_icon="🔑")

st.title("🔑 Toplu API Key Test Cihazı")
st.write("Elinizdeki tüm anahtarları alt alta yapıştırın, hangileri sağlam bulalım.")

# Kullanıcıdan anahtarları al
raw_keys = st.text_area("Anahtarları Buraya Yapıştır (Her satıra bir tane)", height=300)

if st.button("Taramayı Başlat 🚀"):
    if not raw_keys:
        st.error("Hiç anahtar girmedin!")
    else:
        # Anahtarları listeye çevir
        keys_list = [k.strip() for k in raw_keys.split('\n') if k.strip()]
        
        saglam_keys = []
        bozuk_keys = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        st.write("---")
        
        for i, api_key in enumerate(keys_list):
            # İlerleme çubuğunu güncelle
            progress = (i + 1) / len(keys_list)
            progress_bar.progress(progress)
            status_text.text(f"Kontrol ediliyor: {api_key[:10]}...")
            
            try:
                # Bağlantıyı dene
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.0-flash') # veya 1.5-flash
                
                # Ufak bir test isteği at
                response = model.generate_content("Test", request_options={"timeout": 5})
                
                # Hata vermediyse sağlamdır
                st.success(f"✅ ÇALIŞIYOR: {api_key}")
                saglam_keys.append(api_key)
                
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg:
                    st.warning(f"⚠️ KOTA DOLU (Belki yarın çalışır): {api_key}")
                elif "API key not valid" in error_msg:
                    st.error(f"❌ GEÇERSİZ KEY: {api_key}")
                else:
                    st.error(f"❌ HATA: {api_key} - {error_msg}")
                bozuk_keys.append(api_key)
            
            # Google'ı kızdırmamak için 1 saniye bekle
            time.sleep(1)

        st.success("Tarama Bitti!")
        
        if saglam_keys:
            st.markdown("### 💎 SAĞLAM ANAHTARLAR LİSTESİ")
            st.code(str(saglam_keys))
            st.info("Bu listeyi kopyalayıp ana uygulamanın secrets kısmına yapıştırabilirsin!")
        else:
            st.error("Maalesef hiç çalışan anahtar bulunamadı.")