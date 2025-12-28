import streamlit as st
import pandas as pd
import joblib
import os
import base64

# ===============================
# 1. PAGE CONFIGURATION
# ===============================
st.set_page_config(
    page_title="F1 Predictor by Totz",
    page_icon="🏎️",
    layout="wide"
)

# ===============================
# 2. PATH SETUP
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "f1_champion_predictor.pkl")
VIDEO_PATH = os.path.join(BASE_DIR, "background1.mp4")
AUDIO_PATH = os.path.join(BASE_DIR, "theme.mp3")

# ===============================
# 3. 💎 CRYSTAL GLASS CSS (FULLSCREEN FIX) 💎
# ===============================
def apply_glass_theme():
    st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');

    /* GLOBAL STYLES */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* RESET STREAMLIT DEFAULTS */
    .stApp {
        background: transparent !important;
    }
    header {
        background: transparent !important;
    }
    
    /* 1. FORCE FULLSCREEN VIDEO (The Fix) */
    #myVideo {
        position: fixed;
        top: 65%;  /* <--- CHANGED: Was 50%. Increase to move down (Try 60%, 70%) */
        left: 50%;
        min-width: 100%;
        min-height: 120%; /* <--- CHANGED: Increased size to prevent white gap at top */
        width: auto;
        height: auto;
        z-index: -100;
        transform: translateX(-50%) translateY(-50%);
        object-fit: cover;
    }

    /* 2. SIDEBAR - TRUE GLASS EFFECT */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.8) !important;
    }

    /* 3. MAIN CONTAINER - FROSTED CARD */
    .block-container {
        background-color: rgba(0, 0, 0, 0.7); /* Darker for better read */
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem !important;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    /* 4. HEADINGS & TEXT */
    h1 {
        color: #FF1E1E !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 3px 3px 0px #000000;
        text-align: center;
    }
    h2, h3 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
    }
    p, label, .stMarkdown {
        color: #E0E0E0 !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }

    /* 5. INPUT FIELDS */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(5px);
        border-radius: 8px !important;
    }
    input { color: white !important; }

    /* 6. BUTTONS */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #FF1E1E 0%, #B30000 100%);
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.8rem !important;
        font-size: 1.1rem !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
        text-transform: uppercase;
        box-shadow: 0 4px 15px rgba(255, 30, 30, 0.4);
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 30, 30, 0.6);
    }
    
    /* 7. DATAFRAME */
    div[data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_glass_theme()

# ===============================
# 4. BACKGROUND MEDIA (Absolute Center Fix)
# ===============================
def add_bg_media():
    video_b64 = ""
    audio_html = ""
    
    # Load Video
    if os.path.exists(VIDEO_PATH):
        try:
            with open(VIDEO_PATH, "rb") as v_file:
                video_b64 = base64.b64encode(v_file.read()).decode()
        except: pass

    # Load Audio
    if os.path.exists(AUDIO_PATH):
        try:
            with open(AUDIO_PATH, "rb") as a_file:
                audio_b64 = base64.b64encode(a_file.read()).decode()
                audio_html = f'<audio autoplay loop><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
        except: pass

    # CSS to Force Fullscreen Video
    if video_b64:
        st.markdown(f"""
        <video autoplay muted loop id="myVideo">
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
        {audio_html}
        """, unsafe_allow_html=True)

add_bg_media()

# ===============================
# 5. LOAD MODEL
# ===============================
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"❌ Model missing: `{MODEL_PATH}`")
        st.stop()
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ===============================
# 6. APP CONTENT
# ===============================

st.sidebar.title("🏁 MENU")
page = st.sidebar.radio("Go to", ["Home", "Predict from File", "Custom Prediction", "Tech Stack"])
st.sidebar.markdown("---")
st.sidebar.caption("By Totz 🚀")

# --- HOME ---
if page == "Home":
    st.title("F1 CHAMPIONSHIP AI")
    st.markdown("### The Future of Race Strategy")
    st.write("Welcome to the ultimate F1 prediction dashboard. Using Machine Learning to predict the next World Champion.")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.info("👈 Use the **Sidebar** to navigate")
    with c2:
        st.success("📂 Start with **Predict from File**")

# --- PREDICT FROM FILE ---
elif page == "Predict from File":
    st.title("📂 SEASON PREDICTION")
    st.write("Upload your 2025 season CSV data below.")
    
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required = ["driver", "team", "points", "wins", "podiums"]
            
            if not all(col in df.columns for col in required):
                st.error("⚠️ Missing required columns!")
            else:
                features = ["points", "wins", "podiums"]
                probs = model.predict_proba(df[features])[:, 1]
                df["Win Probability (%)"] = probs * 100
                winner = df.loc[df["Win Probability (%)"].idxmax()]
                
                st.divider()
                st.markdown(f"<h1 style='font-size: 3rem;'>🏆 {winner['driver'].upper()} 🏆</h1>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center; color: #FFD700 !important;'>{winner['team']}</h3>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("TOTAL POINTS", winner['points'])
                c2.metric("RACE WINS", winner['wins'])
                c3.metric("WIN PROBABILITY", f"{winner['Win Probability (%)']:.1f}%")
                
                if winner['Win Probability (%)'] > 50:
                    st.balloons()
                
                st.write("")
                st.markdown("### 📊 Championship Leaderboard")
                st.dataframe(df.sort_values("Win Probability (%)", ascending=False).head(10), use_container_width=True)
                
        except Exception as e:
            st.error(f"Error: {e}")

# --- CUSTOM PREDICTION ---
elif page == "Custom Prediction":
    st.title("🎮 DRIVER SIMULATOR")
    st.write("Enter your stats to test the AI model.")
    
    col1, col2, col3 = st.columns(3)
    with col1: points = st.number_input("TOTAL POINTS", 0.0, 600.0, 350.0)
    with col2: wins = st.slider("TOTAL WINS", 0, 25, 5)
    with col3: podiums = st.slider("TOTAL PODIUMS", 0, 25, 12)
    
    if st.button("PREDICT RESULT"):
        input_data = pd.DataFrame([[points, wins, podiums]], columns=["points", "wins", "podiums"])
        prob = model.predict_proba(input_data)[0][1]
        
        st.divider()
        if prob > 0.15:
            st.success(f"🏆 CHAMPION MATERIAL! (Probability: {prob:.1%})")
            st.balloons()
        else:
            st.error(f"❌ NOT A CHAMPION (Probability: {prob:.1%})")

# --- TECH STACK ---
elif page == "Tech Stack":
    st.title("🛠️ TECH STACK")
    st.write("Python • Streamlit • XGBoost • Pandas")
    st.info("Developed by Totz")
