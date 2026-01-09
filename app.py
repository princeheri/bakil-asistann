import streamlit as st
import google.generativeai as genai
import os

# --- AYARLAR ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        # Lokal çalışma için uyarı, hata vermemesi için pass geçiyoruz
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
model = genai.GenerativeModel('gemini-2.5-flash', system_instruction=gizli_talimat)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Bakıl AI", page_icon="☀️", layout="centered", initial_sidebar_state="collapsed")

# --- CSS TASARIMI (%100 OKUNAKLI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* 1. Genel Sayfa Arka Planı (Koyu Lacivert) */
    .stApp {
        background-color: #0f172a;
        font-family: 'Roboto', sans-serif;
    }

    /* 2. Başlık Stili */
    .baslik {
        font-size: 45px;
        font-weight: 800;
        text-align: center;
        color: #38bdf8;
        margin-bottom: 5px;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 10px;
    }
    
    /* Alt Başlık */
    .stCaption {
        color: #cbd5e1 !important;
        font-size: 16px !important;
        text-align: center;
        margin-bottom: 20px;
    }

    /* 3. Mesaj Balonları */
    .stChatMessage {
        background-color: #1e293b !important;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        color: #ffffff !important;
        font-size: 16px;
    }

    /* Kullanıcı Mesajı Arka Planı */
    div[data-testid="stChatMessage"][data-testid="user-message"] {
        background-color: #334155 !important;
    }

    /* 4. Yazı Yazma Kutusu (Input) - BEYAZ ZEMİN */
    .stChatInputContainer textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 8px;
        font-weight: 600;
    }
    
    .stChatInputContainer textarea::placeholder {
        color: #64748b !important;
    }

    /* 5. Butonlar */
    .stButton > button {
        background-color: #38bdf8;
        color: #0f172a !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #ffffff;
        color: #000000 !important;
        transform: scale(1.05);
    }

    /* 6. İmza */
    .alt-imza {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #0f172a;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        color: #94a3b8;
        border-top: 1px solid #334155;
        z-index: 100;
    }
    
    /* Gereksiz Elementleri Gizle */
    header, footer, #MainMenu {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown('<div class="baslik">BAKIL AI</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- BUTONLAR ---
col1, col2, col3 = st.columns(3)

if col1.button("💡 Fikrekê Bide"):
    prompt = "Ji bo îro fikrekî cûda û xweş bide min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("Hata.")

if col2.button("📝 Helbest"):
    prompt = "Li ser welat û hêvîyê helbesteke kurt binivîse."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("Hata.")

if col3.button("🧠 Agahî"):
    prompt = "3 agahiyên balkêş û kurt bêje min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("Hata.")

# --- GEÇMİŞ ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ VE CEVAP ---
if prompt := st.chat_input("Li vir binivîse..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("..."):
            try:
                response = model.generate_content(prompt)
                placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                placeholder.error(f"Hata: {e}")

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
