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

# ===============================
# 3. 💎 CRYSTAL GLASS CSS 💎
# ===============================
def apply_glass_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* Transparent App Background */
    .stApp { background: transparent !important; }
    header { background: transparent !important; }

    /* 1. FORCE FULLSCREEN VIDEO BACKGROUND */
    #myVideo {
        position: fixed;
        top: 65%;           /* Pushed down as requested */
        left: 50%;
        min-width: 100%;
        min-height: 120%;   /* Extra height to cover gaps */
        width: auto;
        height: auto;
        transform: translateX(-50%) translateY(-50%);
        object-fit: cover;
        z-index: -100;      /* Sends it behind everything */
    }

    /* 2. SIDEBAR - GLASS EFFECT */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.8) !important;
    }

    /* 3. MAIN CARD */
    .block-container {
        background-color: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem !important;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }

    /* 4. TEXT STYLES */
    h1 {
        color: #FF1E1E !important;
        text-shadow: 3px 3px 0px #000000;
        text-align: center;
        text-transform: uppercase;
        font-weight: 900 !important;
    }
    h2, h3, p, label, .stMarkdown { color: white !important; }

    /* 5. INPUTS & BUTTONS */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
        backdrop-filter: blur(5px);
    }
    input { color: white !important; }

    div.stButton > button {
        background: linear-gradient(90deg, #FF1E1E 0%, #B30000 100%);
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(255, 30, 30, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

apply_glass_theme()

# ===============================
# 4. BACKGROUND VIDEO (WITH SOUND 🔊)
# ===============================
def set_background_video():
    if os.path.exists(VIDEO_PATH):
        try:
            with open(VIDEO_PATH, "rb") as v_file:
                video_b64 = base64.b64encode(v_file.read()).decode()
                
            # Note: Removed 'muted' attribute.
            # 'autoplay' with sound is often blocked by browsers until user interacts.
            st.markdown(f"""
            <video autoplay loop id="myVideo">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error loading video: {e}")

set_background_video()

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
    st.write("Welcome to the ultimate F1 prediction dashboard.")
    st.markdown("---")
    c1, c2 = st.columns(2)
    c1.info("👈 Use Sidebar to navigate")
    c2.success("📂 Start with **Predict from File**")

# --- PREDICT FROM FILE ---
elif page == "Predict from File":
    st.title("📂 SEASON PREDICTION")
    st.write("Upload your 2025 season CSV data.")
    
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
                c1.metric("POINTS", winner['points'])
                c2.metric("WINS", winner['wins'])
                c3.metric("WIN PROBABILITY", f"{winner['Win Probability (%)']:.1f}%")
                
                if winner['Win Probability (%)'] > 50: st.balloons()
                
                st.markdown("### 📊 Leaderboard")
                st.dataframe(df.sort_values("Win Probability (%)", ascending=False).head(10), use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

# --- CUSTOM PREDICTION ---
elif page == "Custom Prediction":
    st.title("🎮 DRIVER SIMULATOR")
    col1, col2, col3 = st.columns(3)
    with col1: points = st.number_input("TOTAL POINTS", 0.0, 600.0, 350.0)
    with col2: wins = st.slider("TOTAL WINS", 0, 25, 5)
    with col3: podiums = st.slider("TOTAL PODIUMS", 0, 25, 12)
    
    if st.button("PREDICT RESULT"):
        input_data = pd.DataFrame([[points, wins, podiums]], columns=["points", "wins", "podiums"])
        prob = model.predict_proba(input_data)[0][1]
        st.divider()
        if prob > 0.15:
            st.success(f"🏆 CHAMPION MATERIAL! ({prob:.1%})")
            st.balloons()
        else:
            st.error(f"❌ NOT A CHAMPION ({prob:.1%})")

# --- TECH STACK ---
elif page == "Tech Stack":
    st.title("🛠️ TECH STACK")
    st.write("Python • Streamlit • XGBoost • Pandas")
    st.info("Developed by Totz")
