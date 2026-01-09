import streamlit as st
import google.generativeai as genai
import os

# --- SAYFA AYARLARI (EN BAŞTA OLMALI) ---
st.set_page_config(page_title="Bakıl AI", page_icon="☀️", layout="centered", initial_sidebar_state="collapsed")

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

# --- MODELİ ZORLA ÇALIŞTIRMA (BRUTE FORCE) ---
# Bu fonksiyon sırayla tüm model isimlerini dener, çalışan ilkini alır.
@st.cache_resource
def get_working_model():
    model_listesi = [
        'gemini-1.5-flash',
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-pro',
        'gemini-1.0-pro',
        'gemini-1.0-pro-001'
    ]
    
    for model_name in model_listesi:
        try:
            # Test amaçlı modeli yükle
            test_model = genai.GenerativeModel(model_name)
            return test_model
        except:
            continue
    return None

model = get_working_model()

if model is None:
    st.error("HATA: Hiçbir model çalıştırılamadı. Lütfen 'requirements.txt' dosyasında 'google-generativeai>=0.5.0' yazdığından emin ol.")
    st.stop()

# --- CSS TASARIMI (BEYAZ ZEMİN - SİYAH YAZI) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* Genel Sayfa */
    .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-family: 'Roboto', sans-serif;
    }

    /* Başlık */
    .baslik {
        font-size: 50px;
        font-weight: 800;
        text-align: center;
        color: #000000;
        margin-bottom: 5px;
        text-transform: uppercase;
        border-bottom: 3px solid #000000;
        padding-bottom: 10px;
    }
    
    .stCaption {
        color: #333333 !important;
        font-size: 16px !important;
        font-weight: bold;
        text-align: center;
    }

    /* Mesaj Kutuları */
    .stChatMessage {
        background-color: #f4f4f4 !important; /* Açık Gri */
        border: 1px solid #dddddd;
        border-radius: 10px;
        color: #000000 !important;
    }
    
    div[data-testid="stChatMessage"][data-testid="user-message"] {
        background-color: #e0f7fa !important; /* Açık Mavi */
        color: #000000 !important;
    }
    
    .stMarkdown, p {
        color: #000000 !important;
    }

    /* Input Alanı */
    .stChatInputContainer textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 8px;
    }
    
    /* Butonlar */
    .stButton > button {
        background-color: #ffffff;
        color: #000000 !important;
        border: 2px solid #000000;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #000000;
        color: #ffffff !important;
    }

    /* İmza */
    .alt-imza {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: #f4f4f4; text-align: center; padding: 10px;
        font-size: 12px; font-weight: bold; color: #000000;
        border-top: 1px solid #cccccc; z-index: 100;
    }
    header, footer, #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- ARAYÜZ ---
st.markdown('<div class="baslik">BAKIL AI</div>', unsafe_allow_html=True)
st.caption("🚀 Asîstanê Te Yê Zîrek")

# --- GEÇMİŞ YÖNETİMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Silav! Navê min Bakıl e. Ez çawa dikarim alîkariya te bikim?"}
    ]

# --- FONKSİYON: GÜVENLİ MESAJ GÖNDERME ---
def generate_response(prompt_text):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    
    full_prompt = gizli_talimat + "\n\nUser: " + prompt_text
    
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Üzgünüm, bir hata oluştu: {e}"

# --- BUTONLAR ---
col1, col2, col3 = st.columns(3)

if col1.button("💡 Fikrekê Bide", key="b1"):
    cevap = generate_response("Ji bo îro fikrekî cûda û xweş bide min.")
    st.session_state.messages.append({"role": "assistant", "content": cevap})
    st.rerun()

if col2.button("📝 Helbest", key="b2"):
    cevap = generate_response("Li ser welat û hêvîyê helbesteke kurt binivîse.")
    st.session_state.messages.append({"role": "assistant", "content": cevap})
    st.rerun()

if col3.button("🧠 Agahî", key="b3"):
    cevap = generate_response("3 agahiyên balkêş û kurt bêje min.")
    st.session_state.messages.append({"role": "assistant", "content": cevap})
    st.rerun()

# --- SOHBETİ GÖSTER ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ ALANI ---
if prompt := st.chat_input("Li vir binivîse..."):
    # Kullanıcıyı göster
    st.chat_message("user").markdown(prompt)
    
    # Cevabı üret
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("..."):
            cevap = generate_response(prompt)
            placeholder.markdown(cevap)
            st.session_state.messages.append({"role": "assistant", "content": cevap})

# --- İMZA ---
st.markdown('<div class="alt-imza">DESIGNED BY HANİF TOPRAK</div>', unsafe_allow_html=True)
            
