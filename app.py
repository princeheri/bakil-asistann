import streamlit as st
import google.generativeai as genai
import os

# --- AYARLAR ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        # Lokal çalışma için
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

# --- MODEL SEÇİMİ (GARANTİ ÇALIŞAN MODEL) ---
# 'gemini-1.5-flash' hata verdiği için en stabil model olan 'gemini-pro' kullanıyoruz.
try:
    model = genai.GenerativeModel('gemini-pro') # system_instruction gemini-pro'da farklı çalışabilir, burada basit tutuyoruz.
    
    # Not: gemini-pro 'system_instruction' parametresini doğrudan desteklemeyebilir,
    # bu yüzden talimatı chat geçmişine ekleyeceğiz.
except:
    st.error("Model yüklenemedi.")

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bakıl AI", page_icon="☀️", layout="centered", initial_sidebar_state="collapsed")

# --- %100 NETLİK İÇİN BEYAZ TEMA (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* 1. ANA ARKA PLAN: BEYAZ */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-family: 'Roboto', sans-serif;
    }

    /* 2. BAŞLIK */
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

    /* 3. MESAJ KUTULARI */
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

    /* 4. YAZI YAZMA ALANI */
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

    /* 5. BUTONLAR */
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

    /* 6. İMZA */
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
st.markdown('<div class="baslik">BAKIL </div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- SOHBET GEÇMİŞİ BAŞLATMA ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Kimlik talimatını ilk mesaj olarak gizlice ekleyelim (Gemini Pro için)
    st.session_state.chat = model.start_chat(history=[
        {"role": "user", "parts": [gizli_talimat]},
        {"role": "model", "parts": ["Fêm bû. Ez Bakıl im, asîstanê te yê Kurdî."]}
    ])
    # Ekranda görünecek ilk mesaj
    st.session_state.messages.append({"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"})

# --- BUTONLAR ---
col1, col2, col3 = st.columns(3)

def send_message(prompt_text):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.spinner("..."):
        try:
            # Gemini Pro sohbet oturumunu kullan
            response = st.session_state.chat.send_message(prompt_text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"Hata: {e}")

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

# --- INPUT ALANI ---
if prompt := st.chat_input("Li vir binivîse..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                placeholder.error(f"Hata: {e}")

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
    
