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
VIDEO_PATH = os.path.join(BASE_DIR, "background1.mp4") # Ensure this file exists
AUDIO_PATH = os.path.join(BASE_DIR, "theme.mp3")       # Ensure this file exists

# ===============================
# 3. 🔥 THE ULTIMATE GLASSY CSS 🔥
# ===============================
def apply_glass_theme():
    st.markdown("""
    <style>
    /* IMPORT FONT (Orbitron for F1 Tech feel, Poppins for body) */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Poppins:wght@400;600;800&display=swap');

    /* 1. GLOBAL TEXT STYLES (High Visibility) */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        color: #FFFFFF !important;
        text-shadow: 0px 0px 10px rgba(0,0,0,0.8), 2px 2px 0px #FF0000 !important; /* Red Shadow for F1 Vibe */
        letter-spacing: 1px;
    }

    p, li, label, .stMarkdown, .stText {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        text-shadow: 2px 2px 4px #000000 !important; /* Black outline for readability */
        font-size: 1.1rem !important;
    }

    /* 2. GLASSY SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 10, 10, 0.75) !important; /* Dark semi-transparent */
        backdrop-filter: blur(15px) !important; /* The Blur Effect */
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar Text specific */
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] p {
        text-shadow: none !important;
    }

    /* 3. MAIN CONTAINER GLASS CARD */
    .block-container {
        background-color: rgba(0, 0, 0, 0.65); /* Dark Glass */
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem !important;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    /* 4. INPUT FIELDS GLASSY LOOK */
    /* Text Inputs & Number Inputs */
    div[data-baseweb="input"] > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        backdrop-filter: blur(5px);
    }
    /* Sliders */
    div[data-baseweb="slider"] > div {
        background: transparent !important;
    }

    /* 5. BUTTONS (Neon Glow) */
    div.stButton > button {
        background: linear-gradient(45deg, #FF0000, #800000) !important;
        color: white !important;
        border: none !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 1.2rem !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.6);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(255, 0, 0, 1);
    }

    /* 6. DATAFRAME / TABLE STYLING */
    div[data-testid="stDataFrame"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_glass_theme()

# ===============================
# 4. BACKGROUND VIDEO & MUSIC
# ===============================
def add_bg_media():
    video_b64 = ""
    audio_html = ""
    
    if os.path.exists(VIDEO_PATH):
        try:
            with open(VIDEO_PATH, "rb") as v_file:
                video_b64 = base64.b64encode(v_file.read()).decode()
        except: pass

    if os.path.exists(AUDIO_PATH):
        try:
            with open(AUDIO_PATH, "rb") as a_file:
                audio_b64 = base64.b64encode(a_file.read()).decode()
                audio_html = f'<audio autoplay loop><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
        except: pass

    if video_b64:
        st.markdown(f"""
        <style>
        .stApp {{ background: transparent; }}
        #myVideo {{ position: fixed; right: 0; bottom: 0; min-width: 100%; min-height: 100%; z-index: -1; object-fit: cover; }}
        </style>
        <video autoplay muted loop id="myVideo"><source src="data:video/mp4;base64,{video_b64}" type="video/mp4"></video>
        {audio_html}
        """, unsafe_allow_html=True)

add_bg_media()

# ===============================
# 5. LOAD MODEL
# ===============================
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"❌ Model file missing at: `{MODEL_PATH}`")
        st.stop()
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ===============================
# 6. APP LOGIC
# ===============================
st.sidebar.title("🏎️ F1 MENU")
page = st.sidebar.radio("Navigate", ["Home", "Predict from File", "Custom Prediction", "Tech Stack", "About"])
st.sidebar.markdown("---")
st.sidebar.caption("Developed by **Totz** 🚀")

# --- HOME ---
if page == "Home":
    st.title("🏁 F1 CHAMPIONSHIP AI")
    st.markdown("### The Future of Race Prediction")
    st.write("Welcome to the most advanced F1 prediction tool. Using 15 years of data to find the next World Champion.")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.info("👈 Use the **Sidebar** to navigate.")
    with col2:
        st.success("📂 Select **Predict from File** to start.")

# --- PREDICT FROM FILE ---
elif page == "Predict from File":
    st.title("📂 SEASON PREDICTION")
    st.write("Upload your 2025 season CSV data.")
    
    uploaded_file = st.file_uploader("Choose CSV", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            required = ["driver", "team", "points", "wins", "podiums"]
            missing = [col for col in required if col not in df.columns]
            
            if missing:
                st.error(f"⚠️ Missing columns: {', '.join(missing)}")
            else:
                features = ["points", "wins", "podiums"]
                probs = model.predict_proba(df[features])[:, 1]
                df["Win Probability (%)"] = probs * 100
                winner = df.loc[df["Win Probability (%)"].idxmax()]
                
                st.divider()
                st.markdown(f"<h1 style='text-align: center; font-size: 3rem;'>🏆 {winner['driver'].upper()} 🏆</h1>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center; color: #ddd !important;'>{winner['team']}</h3>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("POINTS", winner['points'])
                c2.metric("WINS", winner['wins'])
                c3.metric("WIN CHANCE", f"{winner['Win Probability (%)']:.1f}%")
                
                if winner['Win Probability (%)'] > 50:
                    st.balloons()
                
                st.markdown("### 📊 LEADERBOARD")
                st.dataframe(df.sort_values("Win Probability (%)", ascending=False).head(10), use_container_width=True)
                
        except Exception as e:
            st.error(f"Error: {e}")

# --- CUSTOM PREDICTION ---
elif page == "Custom Prediction":
    st.title("🎮 DRIVER SIMULATOR")
    st.write("Enter stats to test your championship chances.")
    
    col1, col2, col3 = st.columns(3)
    with col1: points = st.number_input("TOTAL POINTS", 0.0, 600.0, 350.0)
    with col2: wins = st.slider("TOTAL WINS", 0, 25, 5)
    with col3: podiums = st.slider("TOTAL PODIUMS", 0, 25, 12)
    
    if st.button("CALCULATE ODDS"):
        input_data = pd.DataFrame([[points, wins, podiums]], columns=["points", "wins", "podiums"])
        prob = model.predict_proba(input_data)[0][1]
        
        st.divider()
        if prob > 0.15:
            st.markdown(f"<h2 style='color: #00ff00 !important; text-align: center;'>🏆 CHAMPION MATERIAL ({prob:.1%})</h2>", unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown(f"<h2 style='color: #ff4444 !important; text-align: center;'>❌ NOT ENOUGH ({prob:.1%})</h2>", unsafe_allow_html=True)

# --- INFO PAGES ---
elif page == "Tech Stack":
    st.title("🛠️ TECH STACK")
    st.write("Python • Streamlit • XGBoost • Pandas")
elif page == "About":
    st.title("ℹ️ ABOUT")
    st.write("AI F1 Predictor | Developed by Totz")
