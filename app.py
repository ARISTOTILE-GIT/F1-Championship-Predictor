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
# 2. PATH SETUP (THE FIX)
# ===============================
# This gets the absolute path of the folder where app.py is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths to your files
MODEL_PATH = os.path.join(BASE_DIR, "f1_champion_predictor.pkl")
VIDEO_PATH = os.path.join(BASE_DIR, "background1.mp4")
AUDIO_PATH = os.path.join(BASE_DIR, "theme.mp3")

# ===============================
# 3. BACKGROUND MEDIA (Optional)
# ===============================
def add_bg_media():
    video_b64 = ""
    audio_html = ""
    
    # Try loading video
    if os.path.exists(VIDEO_PATH):
        try:
            with open(VIDEO_PATH, "rb") as v_file:
                video_b64 = base64.b64encode(v_file.read()).decode()
        except: pass

    # Try loading audio
    if os.path.exists(AUDIO_PATH):
        try:
            with open(AUDIO_PATH, "rb") as a_file:
                audio_b64 = base64.b64encode(a_file.read()).decode()
                audio_html = f'<audio autoplay loop><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'
        except: pass

    # Apply CSS only if video exists
    if video_b64:
        st.markdown(f"""
        <style>
        .stApp {{ background: transparent; }}
        #myVideo {{ position: fixed; right: 0; bottom: 0; min-width: 100%; min-height: 100%; z-index: -1; opacity: 0.8; }}
        .block-container {{ background-color: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 2rem; margin-top: 2rem; }}
        h1, h2, h3, p, li, label {{ color: #333333 !important; }}
        </style>
        <video autoplay muted loop id="myVideo"><source src="data:video/mp4;base64,{video_b64}" type="video/mp4"></video>
        {audio_html}
        """, unsafe_allow_html=True)

add_bg_media()

# ===============================
# 4. LOAD MODEL
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
# 5. NAVIGATION
# ===============================
st.sidebar.title("🏎️ F1 Predictor")
page = st.sidebar.radio("Navigate", ["Home", "Predict from File", "Custom Prediction", "Tech Stack", "About"])
st.sidebar.markdown("---")
st.sidebar.caption("Developed by **Totz** 🚀")

# ===============================
# PAGE: HOME
# ===============================
if page == "Home":
    st.title("🏁 F1 Championship AI")
    st.markdown("### The Ultimate AI Predictor")
    st.write("Welcome to the most advanced F1 prediction tool. Upload data, analyze stats, and find the next World Champion.")
    st.success("👈 Select **'Predict from File'** in the sidebar to start!")

# ===============================
# PAGE: PREDICT FROM FILE
# ===============================
elif page == "Predict from File":
    st.title("📂 Upload Season CSV")
    st.write("Upload your 2025 season data to predict the winner.")
    
    # FILE UPLOADER (Shown immediately)
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Check columns
            required = ["driver", "team", "points", "wins", "podiums"]
            missing = [col for col in required if col not in df.columns]
            
            if missing:
                st.error(f"⚠️ Missing columns: {', '.join(missing)}")
            else:
                st.success("File uploaded! Analyzing...")
                
                # PREDICTION LOGIC
                features = ["points", "wins", "podiums"]
                probs = model.predict_proba(df[features])[:, 1]
                df["Win Probability (%)"] = probs * 100
                
                # Get Winner
                winner = df.loc[df["Win Probability (%)"].idxmax()]
                
                st.divider()
                st.markdown(f"<h1 style='text-align: center; color: #D32F2F;'>🏆 {winner['driver']}</h1>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{winner['team']}</h3>", unsafe_allow_html=True)
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Points", winner['points'])
                c2.metric("Wins", winner['wins'])
                c3.metric("Win Chance", f"{winner['Win Probability (%)']:.1f}%")
                
                if winner['Win Probability (%)'] > 50:
                    st.balloons()
                
                st.subheader("Full Standings")
                st.dataframe(df.sort_values("Win Probability (%)", ascending=False), use_container_width=True)
                
        except Exception as e:
            st.error(f"Error processing file: {e}")

# ===============================
# PAGE: CUSTOM PREDICTION
# ===============================
elif page == "Custom Prediction":
    st.title("🎮 Custom Prediction")
    
    col1, col2, col3 = st.columns(3)
    with col1: points = st.number_input("Points", 0.0, 600.0, 350.0)
    with col2: wins = st.slider("Wins", 0, 25, 5)
    with col3: podiums = st.slider("Podiums", 0, 25, 12)
    
    if st.button("Predict"):
        input_data = pd.DataFrame([[points, wins, podiums]], columns=["points", "wins", "podiums"])
        prob = model.predict_proba(input_data)[0][1]
        
        st.divider()
        if prob > 0.15:
            st.success(f"🏆 Champion! Probability: {prob:.2%}")
            st.balloons()
        else:
            st.error(f"❌ Not a Champion. Probability: {prob:.2%}")

# ===============================
# PAGE: TECH STACK
# ===============================
elif page == "Tech Stack":
    st.title("🛠️ Tech Stack")
    st.write("Python, Streamlit, XGBoost, Pandas, Scikit-learn")

elif page == "About":
    st.title("ℹ️ About")
    st.write("F1 Predictor Project (2010-2024 Data)")
    st.caption("Developed by Totz")
