import streamlit as st
import google.generativeai as genai

st.title("Gemini Model Rehberi 🔍")

# API Key Girişi
api_key = st.text_input("API Key'inizi buraya yapıştırın:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        
        st.success("Bağlantı Başarılı! Kullanabileceğin Modeller:")
        
        # Modelleri listele
        model_list = []
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                model_list.append(m.name)
        
        st.write(model_list)
        
        # Tavsiye
        st.info("💡 **Startup Survivor** için bu listede 'pro' veya 'thinking' (varsa) geçen en güncel modeli seçmeliyiz.")

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
else:
    st.warning("Lütfen API Key girin.")