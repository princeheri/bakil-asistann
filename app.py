import streamlit as st
import google.generativeai as genai
import os

# --- AYARLAR ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.warning("API Anahtarı bulunamadı! Streamlit Secrets ayarlarını kontrol et.")
except FileNotFoundError:
    st.error("Secrets dosyası bulunamadı.")

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

# --- %100 OKUNAKLI CSS TASARIMI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* 1. Genel Sayfa Arka Planı (Koyu Lacivert - Mat) */
    .stApp {
        background-color: #0f172a; /* Çok koyu, mat lacivert */
        font-family: 'Roboto', sans-serif;
    }

    /* 2. Başlık Stili */
    .baslik {
        font-size: 45px;
        font-weight: 800;
        text-align: center;
        color: #38bdf8; /* Parlak Açık Mavi */
        margin-bottom: 5px;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-bottom: 2px solid #38bdf8;
        padding-bottom: 10px;
    }
    
    /* Alt Başlık Rengi */
    .stCaption {
        color: #cbd5e1 !important; /* Açık gri */
        font-size: 16px !important;
        text-align: center;
        margin-bottom: 20px;
    }

    /* 3. Mesaj Balonları (Net Okunabilirlik İçin) */
    /* Asistan Mesajı */
    .stChatMessage {
        background-color: #1e293b !important; /* Daha açık lacivert */
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 15px;
        color: #ffffff !important; /* BEYAZ YAZI */
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* Kullanıcı Mesajı */
    div[data-testid="stChatMessage"] {
        background-color: #334155;
    }

    /* 4. Yazı Yazma Kutusu (Input) - EN ÖNEMLİSİ */
    .stChatInputContainer textarea {
        background-color: #ffffff !important; /* Arka plan BEYAZ */
        color: #000000 !important; /* Yazı SİYAH */
        border: 2px solid #38bdf8 !important; /* Mavi Çerçeve */
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Placeholder (Silik yazı rengi) */
    .stChatInputContainer textarea::placeholder {
        color: #64748b !important;
    }

    /* 5. Butonlar (Yüksek Kontrast) */
    .stButton > button {
        background-color: #38bdf8; /* Parlak Mavi Buton */
        color: #0f172a !important; /* Koyu Lacivert Yazı */
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: transform 0.2s;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #ffffff; /* Üzerine gelince Beyaz */
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
    }
    
    /* Header Gizleme */
    header, footer, #MainMenu {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown('<div class="baslik">BAKIL AI</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- ÖNERİ BUTONLARI ---
col1, col2, col3 = st.columns(3)

if col1.button("💡 Fikrekê Bide"):
    prompt = "Ji bo îro fikrekî cûda û xweş bide min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Wait..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("Hata.")

if col2.button("📝 Helbest"):
    prompt = "Li ser welat û hêvîyê helbesteke kurt binivîse."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Wait..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("Hata.")

if col3.button("🧠 Agahî"):
    prompt = "3 agahiyên balkêş û kurt bêje min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Wait..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("Hata.")


# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ KUTUSU ---
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
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600&display=swap');

    /* Genel Sayfa Yapısı */
    .stApp {
        background: linear-gradient(135deg, #140d2b 0%, #2e2a5c 100%);
        font-family: 'Montserrat', sans-serif;
        color: #ffffff;
    }
    
    /* Üst Başlık ve Footer Gizleme */
    header, footer, #MainMenu {visibility: hidden;}

    /* Başlık Stili (Altın Sarısı Efekt) */
    .baslik {
        font-size: 50px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(to right, #FFD700, #FDB931, #C0C0C0, #FDB931, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }

    /* Mesaj Balonları (Okunabilirlik İçin Koyu Arka Plan) */
    .stChatMessage {
        background-color: rgba(0, 0, 0, 0.4) !important; /* Yarı saydam siyah */
        border: 1px solid rgba(255, 215, 0, 0.2); /* Hafif altın çerçeve */
        border-radius: 15px;
        color: #ffffff !important; /* Yazılar kesinlikle beyaz */
    }

    /* Kullanıcı Mesajı İkonu */
    .stChatMessage[data-testid="user-message"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* Input Alanı (Yazı Yazılan Yer - En Önemli Kısım) */
    .stChatInputContainer textarea {
        background-color: #1e1e2f !important; /* Koyu Gri Arka Plan */
        color: #ffffff !important; /* Beyaz Yazı */
        border: 1px solid #FFD700 !important; /* Altın Çerçeve */
        border-radius: 10px;
    }
    
    /* Input Alanı Placeholder (Silik Yazı) Rengi */
    .stChatInputContainer textarea::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }

    /* Butonlar */
    .stButton > button {
        background: linear-gradient(to right, #1e1e2f, #2e2a5c);
        color: #FFD700 !important; /* Altın Sarısı Yazı */
        border: 1px solid #FFD700;
        border-radius: 20px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        background: #FFD700;
        color: #000 !important; /* Üzerine gelince siyah yazı */
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
        border: 1px solid transparent;
    }

    /* Alt İmza */
    .alt-imza {
        position: fixed;
        bottom: 10px;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 12px;
        color: rgba(255,255,255,0.4);
        letter-spacing: 2px;
        z-index: 99;
        pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown('<div class="baslik">BAKIL</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- ÖNERİ BUTONLARI ---
col1, col2, col3 = st.columns(3)

if col1.button("💡 Fikrekê Bide"):
    prompt = "Ji bo îro fikrekî cûda û xweş bide min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Tê fikirîn..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("Hata oluştu.")

if col2.button("📝 Helbest"):
    prompt = "Li ser welat û hêvîyê helbesteke kurt binivîse."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Tê nivîsandin..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("Hata oluştu.")

if col3.button("🧠 Agahî"):
    prompt = "3 agahiyên balkêş û kurt bêje min."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Tê lêkolîn..."):
        try:
            response = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except:
            st.error("Hata oluştu.")


# --- SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ KUTUSU ---
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
                placeholder.error(f"Pirsgirêk: {e}")

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
