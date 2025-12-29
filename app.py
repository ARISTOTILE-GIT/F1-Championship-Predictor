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
# 3. F1 STYLING (FIXED VISIBILITY) 🎨
# ===============================
st.markdown("""
<style>
    /* 1. IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* 2. FORCE LIGHT THEME (Fixes Dark Text Issue) */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* 3. F1 STYLE HEADINGS */
    h1, h2, h3 {
        font-family: 'Titillium Web', sans-serif !important;
        text-transform: uppercase;
        font-style: italic;
        letter-spacing: 1px;
    }
    
    h1 {
        color: #E10600 !important; /* F1 Red */
        font-weight: 900 !important;
        font-size: 3rem !important;
    }
    
    h2 {
        color: #15151e !important; /* Dark Carbon */
        font-weight: 900 !important;
        /* Removed border-bottom (The Red Line) */
        padding-bottom: 5px;
    }
    
    h3 {
        color: #333333 !important;
    }
    
    /* 4. BODY TEXT (High Contrast) */
    p, label, li, .stMarkdown, .stText, div {
        font-family: 'Roboto', sans-serif;
        color: #000000 !important; /* Pure Black for maximum readability */
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* 5. METRIC CARDS */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa !important; /* Light Grey Card */
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] {
        color: #666 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #15151e !important;
        font-size: 2rem !important;
    }
    
    /* 6. BUTTONS */
    div.stButton > button {
        background-color: #E10600 !important;
        color: white !important;
        font-family: 'Titillium Web', sans-serif;
        font-weight: 900;
        font-style: italic;
        text-transform: uppercase;
        border-radius: 5px;
        border: none;
        padding: 0.6rem 2rem;
        font-size: 1.2rem;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #ff1a1a !important;
        transform: translateY(-2px);
    }
    
    /* 7. SIDEBAR */
    section[data-testid="stSidebar"] { 
        background-color: #15151e !important; /* Dark Sidebar */
    }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: #f0f0f0 !important; /* White text for sidebar only */
    }
    
    /* 8. ALERTS/INFO BOXES - Fix Text Color */
    .stAlert {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# 4. SIDEBAR NAVIGATION
# ===============================
st.sidebar.title("🏎️ ANALYTICS HUB")

# Removed "Model Insights" from the list
page = st.sidebar.radio(
    "MENU", 
    ["🏠 Home", "🔮 Predict Season", "🆚 Driver Comparison", "🎮 Simulator", "🛠️ Tech Stack"]
)

st.sidebar.markdown("---")
st.sidebar.info("Developed by **Totz** 🚀")

# ===============================
# PAGE: HOME
# ===============================
if page == "🏠 Home":
    # Hero Title
    st.markdown("<h1 style='text-align: center;'>FORMULA 1 CHAMPIONSHIP PREDICTOR & SIMULATOR</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555 !important;'>Season Prediction • Driver Comparison • Championship Simulator</h3>", unsafe_allow_html=True)
    st.divider()

    # Intro
    st.markdown("""
    This application uses **Machine Learning** to analyze Formula 1 driver performance and predict championship outcomes.
    
    You can predict the season winner, **compare** drivers side-by-side, and simulate **custom** scenarios to understand how points, wins, and podiums influence the title race.
    """)
    st.write("") 

    # Core Features
    st.markdown("## 🚀 CORE FEATURES")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🔮 **Season Winner Prediction**")
        st.markdown("Upload season-level driver statistics to predict the most likely Formula 1 World Champion with probability scores.")
        
    with col2:
        st.warning("🆚 **Driver Comparison**")
        st.markdown("Compare two drivers based on their performance metrics and AI-generated championship probabilities.")
        
    with col3:
        st.success("🎮 **Championship Simulator**")
        st.markdown("Create your own driver scenario by adjusting points, wins, and podiums to simulate different championship outcomes.")

    st.write("")

    # AI Section
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("## ⚙️ HOW THE AI WORKS")
        st.markdown("""
        1️⃣ Performance data is collected for each driver.  
        2️⃣ The trained ML model evaluates historical patterns (**2010–2024**).  
        3️⃣ Probability scores are generated for championship success.  
        4️⃣ Results are presented for prediction, comparison, and simulation.
        """)
        
    with c2:
        st.markdown("## 🎯 WHY THIS PROJECT MATTERS")
        st.markdown("""
        This project demonstrates how machine learning can be applied to sports analytics by converting raw race data into meaningful championship insights.
        """)

    st.divider()

    # Call to Action
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
            st.markdown("### 🤖 AI VERDICT")
            if d1['Win Probability'] > d2['Win Probability']:
                st.success(f"**{d1['driver']}** has a statistically higher chance of winning.")
            elif d2['Win Probability'] > d1['Win Probability']:
                st.success(f"**{d2['driver']}** leads the prediction model with stronger performance.")
            else:
                st.info("It's a dead heat! Both drivers have identical probabilities.")

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
            elif prob > 20: st.info("🏎️ **MID-FIELD.** Good season, but not a title winner.")
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
        st.caption("Interactive Web Interface & Dashboarding")
        st.markdown("### 🧠 AI MODEL")
        st.error("**XGBOOST**")
        st.caption("Gradient Boosting Machine Learning Algorithm")
    with col2:
        st.markdown("### 📊 DATA ENGINE")
        st.success("**PANDAS**")
        st.caption("Data Manipulation & Analysis")
        st.markdown("### 🐍 CORE LANGUAGE")
        st.warning("**PYTHON**")
        st.caption("Backend Logic & Integration")
    st.divider()
    st.caption("F1 Championship Predictor Project | Developed by **Totz**")
