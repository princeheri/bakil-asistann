import streamlit as st
import google.generativeai as genai
import os

# --- AYARLAR ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        pass
except FileNotFoundError:
    pass

# --- YAPAY ZEKANIN KİMLİĞİ ---
gizli_talimat = """
Navê te Bakıl e.
Tu asîstanekî zîrek, alîkar û Kurdîaxêv î.
Pêşdebirê te: HANİF TOPRAK. (Heke bipirsin tenê bibêje Hanif Toprak).

ÖNEMLİ TALİMAT (MEMLEKET):
Heke yek ji te bipirse "Tu xelkê ku derê yî?", "Ji ku derê yî?" an bi Tirkî "Nerelisin?", "Nereden geliyorsun?":
Cewaba te teqez ev be: "Ez ji Kurdistanê me" (Heke bi Tirkî pirsîbûn: "Ben Kürdistanlıyım").

Zimanê te yê sereke Kurdî ye, lê tu dikarî bi Tirkî jî biaxivî.
"""

# --- OTOMATİK MODEL SEÇİCİ (HATA ÖNLEYİCİ) ---
# Bu kısım sistemindeki çalışan modelleri tarar ve en iyisini seçer.
def en_iyi_modeli_bul():
    varsayilan = 'gemini-pro'
    try:
        # Sistemdeki tüm modelleri listele
        tum_modeller = genai.list_models()
        # Sadece metin üretebilenleri filtrele
        uygunlar = [m.name for m in tum_modeller if 'generateContent' in m.supported_generation_methods]
        
        # Öncelik sıramız (En hızlıdan en iyiye)
        tercihler = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro',
            'models/gemini-pro',
            'models/gemini-1.0-pro'
        ]
        
        # Tercihlerimizden biri var mı kontrol et
        for tercih in tercihler:
            if tercih in uygunlar:
                return tercih
        
        # Tercihler yoksa, eldeki herhangi bir çalışan modeli seç
        if uygunlar:
            return uygunlar[0]
            
    except Exception as e:
        pass
    
    return varsayilan

# Modeli başlat
secilen_model_ismi = en_iyi_modeli_bul()
try:
    model = genai.GenerativeModel(secilen_model_ismi)
except:
    st.error("Model başlatılamadı. API Anahtarını kontrol et.")

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bakıl AI", page_icon="☀️", layout="centered", initial_sidebar_state="collapsed")

# --- %100 NETLİK İÇİN BEYAZ TEMA (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-family: 'Roboto', sans-serif;
    }
    .baslik {
        font-size: 50px;
        font-weight: 800;
        text-align: center;
        color: #000000;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 3px solid #000000;
        padding-bottom: 10px;
    }
    .stCaption {
        color: #444444 !important;
        font-size: 16px !important;
        font-weight: bold;
        text-align: center;
    }
    .stChatMessage {
        background-color: #f0f2f6 !important;
        border: 1px solid #cccccc;
        border-radius: 10px;
        padding: 15px;
        color: #000000 !important;
    }
    div[data-testid="stChatMessage"][data-testid="user-message"] {
        background-color: #e3f2fd !important;
        color: #000000 !important;
    }
    .stMarkdown, .stMarkdown p {
        color: #000000 !important;
    }
    .stChatInputContainer textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 8px;
        font-weight: 600;
    }
    .stChatInputContainer textarea::placeholder {
        color: #666666 !important;
    }
    .stButton > button {
        background-color: #ffffff;
        color: #000000 !important;
        border: 2px solid #000000;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #000000;
        color: #ffffff !important;
    }
    .alt-imza {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f0f2f6;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        font-weight: bold;
        color: #000000;
        border-top: 1px solid #cccccc;
        z-index: 100;
    }
    header, footer, #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown('<div class="baslik">BAKIL AI</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- SOHBET GEÇMİŞİ VE SESSION YÖNETİMİ ---
if "chat" not in st.session_state:
    try:
        st.session_state.chat = model.start_chat(history=[
            {"role": "user", "parts": [gizli_talimat]},
            {"role": "model", "parts": ["Fêm bû. Ez Bakıl im."]}
        ])
    except:
        # Eski kütüphaneler start_chat desteklemeyebilir, manuel yönetim
        pass

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"}
    ]

# --- MESAJ GÖNDERME FONKSİYONU ---
def send_message(prompt_text):
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.spinner("..."):
        try:
            # Önce chat session varsa onu dene
            if "chat" in st.session_state:
                response = st.session_state.chat.send_message(prompt_text)
                text_response = response.text
            else:
                # Yoksa düz generate_content kullan (Eski sürüm uyumluluğu)
                # Talimatı da ekle ki kimliği unutmasın
                full_prompt = gizli_talimat + "\n\nUser: " + prompt_text
                response = model.generate_content(full_prompt)
                text_response = response.text

            st.session_state.messages.append({"role": "assistant", "content": text_response})
            st.rerun()
        except Exception as e:
            st.error(f"Hata: {e}")

# --- BUTONLAR ---
col1, col2, col3 = st.columns(3)

if col1.button("💡 Fikrekê Bide", key="btn_fikir"):
    send_message("Ji bo îro fikrekî cûda û xweş bide min.")

if col2.button("📝 Helbest", key="btn_helbest"):
    send_message("Li ser welat û hêvîyê helbesteke kurt binivîse.")

if col3.button("🧠 Agahî", key="btn_agahi"):
    send_message("3 agahiyên balkêş û kurt bêje min.")

# --- GEÇMİŞİ GÖSTER ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- KULLANICI GİRİŞİ ---
if prompt := st.chat_input("Li vir binivîse..."):
    st.chat_message("user").markdown(prompt)
    
    # Kullanıcı mesajını hemen ekle (Hızlı tepki için)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Cevabı bekle
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("..."):
            try:
                if "chat" in st.session_state:
                    response = st.session_state.chat.send_message(prompt)
                    text_response = response.text
                else:
                    full_prompt = gizli_talimat + "\n\nUser: " + prompt
                    response = model.generate_content(full_prompt)
                    text_response = response.text
                    
                placeholder.markdown(text_response)
                st.session_state.messages.append({"role": "assistant", "content": text_response})
            except Exception as e:
                placeholder.error(f"Hata: {e}")

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
            
