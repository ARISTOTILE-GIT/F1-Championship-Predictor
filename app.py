import streamlit as st
import pandas as pd
import joblib
import os

# ===============================
# 1. PAGE CONFIGURATION
# ===============================
st.set_page_config(
    page_title="F1 Analytics Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# 2. LOAD MODEL & ASSETS
# ===============================
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "f1_champion_predictor.pkl")
    
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

model = load_model()

# ===============================
# 3. F1 STYLING (PURE LIGHT THEME FIXED) 🎨
# ===============================
st.markdown("""
<style>
    /* 1. IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@300;400;600;700;900&display=swap');

    /* 2. UNIVERSAL FONT & COLOR RESET */
    html, body, [class*="css"], font, span, div, p, h1, h2, h3, h4, h5, h6 {
        font-family: 'Titillium Web', sans-serif !important;
        color: #000000 !important; /* Force Black Text Everywhere */
    }

    /* 3. HIDE DEFAULT HEADER */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 4. BACKGROUNDS */
    .stApp {
        background-color: #ffffff !important;
        margin-top: -30px;
    }

    /* 5. HEADINGS */
    h1 {
        color: #E10600 !important; /* F1 Red */
        font-weight: 900 !important;
        font-style: italic;
        text-transform: uppercase;
        font-size: 3.5rem !important;
        letter-spacing: 1px;
    }
    h2 {
        color: #111111 !important;
        font-weight: 800 !important;
        font-style: italic;
        text-transform: uppercase;
    }
    h3 {
        color: #333333 !important;
        font-weight: 700 !important;
    }
    
    /* 6. INPUTS & DROPDOWNS (THE FIX) */
    /* The box itself */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"] {
        background-color: #f8f9fa !important; /* Very Light Grey */
        border: 1px solid #ced4da !important;
        color: #000000 !important;
    }
    
    /* Text inside inputs */
    input[type="text"], input[type="number"], div[data-baseweb="select"] span {
        color: #000000 !important; 
        font-weight: 600 !important;
    }
    
    /* The Dropdown Menu List (When you click it) */
    ul[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #ddd !important;
    }
    li[data-baseweb="menu-item"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    li[data-baseweb="menu-item"]:hover {
        background-color: #f0f0f0 !important;
    }
    
    /* 7. FILE UPLOADER (LIGHT THEME FIX) */
    section[data-testid="stFileUploaderDropzone"] {
        background-color: #f8f9fa !important;
        border: 2px dashed #E10600 !important;
        border-radius: 10px;
    }
    section[data-testid="stFileUploaderDropzone"] div {
        color: #333333 !important;
    }
    section[data-testid="stFileUploaderDropzone"] span {
        color: #333333 !important;
        font-weight: bold;
    }
    /* The 'Browse files' button */
    section[data-testid="stFileUploaderDropzone"] button {
        background-color: #E10600 !important;
        color: #ffffff !important; /* White Text on Button */
        border: none !important;
    }
    /* The Uploaded File Name Box */
    div[data-testid="stFileUploaderFile"] {
        background-color: #ffffff !important;
        border: 1px solid #ddd;
    }
    
    /* 8. BUTTONS */
    div.stButton > button {
        background-color: #E10600 !important;
        color: white !important;
        font-weight: 900 !important;
        font-style: italic;
        text-transform: uppercase;
        border-radius: 5px;
        border: none;
        padding: 0.6rem 2rem;
        font-size: 1.2rem !important;
        box-shadow: 0 4px 0px #b30500;
    }
    div.stButton > button:hover {
        background-color: #ff1a1a !important;
        transform: translateY(-2px);
    }

    /* 9. SIDEBAR */
    section[data-testid="stSidebar"] { 
        background-color: #f4f4f4 !important;
        border-right: 1px solid #ddd;
    }
    /* Sidebar Links (Radio Buttons) */
    div[data-testid="stSidebar"] label {
        color: #000000 !important;
        font-weight: 600;
    }

    /* 10. METRIC CARDS */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0;
        border-left: 5px solid #E10600 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] { color: #666 !important; }
    div[data-testid="stMetricValue"] { color: #000 !important; }

</style>
""", unsafe_allow_html=True)

# ===============================
# 4. SIDEBAR NAVIGATION
# ===============================
st.sidebar.title("🏎️ ANALYTICS HUB")

page = st.sidebar.radio(
    "MENU", 
    ["🏠 Home", "🔮 Predict Season", "🆚 Driver Comparison", "🎮 Simulator", "🛠️ Tech Stack"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Developed by **Totz** 🚀")

# ===============================
# PAGE: HOME
# ===============================
if page == "🏠 Home":
    st.markdown("<h1 style='text-align: center;'>FORMULA 1 CHAMPIONSHIP PREDICTOR & SIMULATOR</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555 !important;'>Season Prediction • Driver Comparison • Championship Simulator</h3>", unsafe_allow_html=True)
    st.divider()

    st.markdown("## ⚙️ HOW THE AI WORKS & WHY THIS PROJECT MATTERS")
    st.markdown("""
    The application analyzes Formula 1 driver performance data using a trained machine learning model based on historical seasons from **2010 to 2024**.

    The model evaluates patterns in **points, wins, and podiums** to generate probability scores that indicate a driver’s likelihood of winning the championship.

    This project demonstrates how machine learning can be effectively applied to sports analytics by transforming raw racing data into meaningful championship insights for prediction, comparison, and simulation.
    """)
    st.write("") 

    st.markdown("## 🚀 CORE FEATURES")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🔮 **Season Winner Prediction**")
        st.markdown("Upload season-level driver statistics to predict the most likely Formula 1 World Champion.")
    with col2:
        st.warning("🆚 **Driver Comparison**")
        st.markdown("Compare two drivers based on their performance metrics and AI-generated probabilities.")
    with col3:
        st.success("🎮 **Championship Simulator**")
        st.markdown("Create your own driver scenario by adjusting points, wins, and podiums.")

    st.divider()
    st.markdown("### 👉 READY TO START?")
    st.success("""
    **Use the sidebar to explore:**
    * 🔮 **Predict from File**
    * 🆚 **Driver Comparison**
    * 🎮 **Custom Prediction Simulator**
    """)

# ===============================
# PAGE: PREDICT SEASON
# ===============================
elif page == "🔮 Predict Season":
    st.title("SEASON PREDICTION")
    st.write("Upload your 2025 dataset to analyze championship odds.")
    
    # Upload Bar is now Light Grey + Red Button via CSS
    uploaded_file = st.file_uploader("Upload CSV (Required: driver, team, points, wins, podiums)", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            required_cols = ["driver", "team", "points", "wins", "podiums"]
            
            if not all(col in df.columns for col in required_cols):
                st.error(f"⚠️ Missing columns! CSV must have: {required_cols}")
            else:
                if model:
                    features = ["points", "wins", "podiums"]
                    probs = model.predict_proba(df[features])[:, 1]
                    df["Win Probability"] = probs
                    df["Win Probability %"] = (probs * 100).round(2)
                    st.session_state['f1_data'] = df
                    winner = df.loc[df["Win Probability"].idxmax()]
                    
                    st.success("Analysis Complete!")
                    st.divider()
                    col_main, col_chart = st.columns([1, 1.5])
                    with col_main:
                        st.markdown("### 🏆 PREDICTED CHAMPION")
                        st.markdown(f"<h1 style='color: #E10600 !important; font-style: italic;'>{winner['driver']}</h1>", unsafe_allow_html=True)
                        st.markdown(f"## {winner['team']}")
                        st.metric("CHAMPIONSHIP PROBABILITY", f"{winner['Win Probability %']}%", delta="Highest Odds")
                    with col_chart:
                        st.markdown("### 📈 PROBABILITY CHART")
                        chart_data = df.sort_values("Win Probability", ascending=False).head(10)
                        st.bar_chart(chart_data.set_index("driver")["Win Probability %"], color="#E10600")
                    st.divider()
                    st.markdown("### 📋 FULL LEADERBOARD")
                    st.dataframe(df.sort_values("Win Probability", ascending=False)[["driver", "team", "points", "wins", "podiums", "Win Probability %"]], use_container_width=True)
                else:
                    st.error("❌ Model not found! Please check 'f1_champion_predictor.pkl'.")
        except Exception as e:
            st.error(f"Error processing file: {e}")

# ===============================
# PAGE: DRIVER COMPARISON
# ===============================
elif page == "🆚 Driver Comparison":
    st.title("HEAD-TO-HEAD BATTLE")
    if 'f1_data' not in st.session_state:
        st.warning("⚠️ Please upload a dataset in the **'Predict Season'** page first.")
    else:
        df = st.session_state['f1_data']
        drivers = df['driver'].unique()
        c1, c2 = st.columns(2)
        with c1: d1_name = st.selectbox("SELECT DRIVER 1", drivers, index=0)
        with c2: d2_name = st.selectbox("SELECT DRIVER 2", drivers, index=1)
            
        if d1_name and d2_name:
            d1 = df[df['driver'] == d1_name].iloc[0]
            d2 = df[df['driver'] == d2_name].iloc[0]
            st.divider()
            col_a, col_mid, col_b = st.columns([1, 0.2, 1])
            with col_a:
                st.markdown(f"<h2 style='text-align: center; color: #E10600 !important;'>{d1['driver']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{d1['team']}</h3>", unsafe_allow_html=True)
                st.metric("WIN PROBABILITY", f"{d1['Win Probability %']}%")
            with col_mid:
                st.markdown("<h1 style='text-align: center; font-size: 50px; color: #ccc !important;'>VS</h1>", unsafe_allow_html=True)
            with col_b:
                st.markdown(f"<h2 style='text-align: center; color: #15151e !important;'>{d2['driver']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{d2['team']}</h3>", unsafe_allow_html=True)
                st.metric("WIN PROBABILITY", f"{d2['Win Probability %']}%")
            st.markdown("### 📊 STAT BREAKDOWN")
            comp_df = pd.DataFrame({
                'METRIC': ['TOTAL POINTS', 'RACE WINS', 'PODIUMS'],
                d1['driver']: [d1['points'], d1['wins'], d1['podiums']],
                d2['driver']: [d2['points'], d2['wins'], d2['podiums']]
            }).set_index('METRIC')
            st.table(comp_df)

# ===============================
# PAGE: SIMULATOR
# ===============================
elif page == "🎮 Simulator":
    st.title("WHAT-IF SIMULATOR")
    st.write("Adjust stats to see how they impact championship odds in real-time.")
    st.markdown("#### ENTER DRIVER STATS")
    c1, c2, c3 = st.columns(3)
    p_in = c1.number_input("TOTAL POINTS", 0.0, 600.0, 350.0, step=10.0)
    w_in = c2.slider("RACE WINS", 0, 25, 5)
    pod_in = c3.slider("PODIUMS", 0, 25, 10)
    if model:
        input_data = pd.DataFrame([[p_in, w_in, pod_in]], columns=["points", "wins", "podiums"])
        prob = model.predict_proba(input_data)[0][1] * 100
        st.divider()
        st.markdown("### SIMULATED OUTCOME")
        col_gauge, col_text = st.columns([1, 2])
        with col_gauge: st.metric("WIN PROBABILITY", f"{prob:.2f}%")
        with col_text:
            if prob > 80: st.success("🏆 **DOMINANT CHAMPION!** These stats guarantee a title.")
            elif prob > 50: st.warning("🔥 **STRONG CONTENDER.** A very close fight.")
            else: st.error("❌ **NO CHANCE.** Needs better results.")

# ===============================
# PAGE: TECH STACK
# ===============================
elif page == "🛠️ Tech Stack":
    st.title("TECHNOLOGY STACK")
    st.write("The modern framework powering this F1 predictor.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💻 FRONTEND")
        st.info("**STREAMLIT**")
    with col2:
        st.markdown("### 🧠 AI MODEL")
        st.error("**XGBOOST**")
    st.divider()
    st.caption("F1 Championship Predictor Project | Developed by **Totz**")
