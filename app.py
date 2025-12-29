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
    # Robust path finding (Works in Root or Codes folder)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "f1_champion_predictor.pkl")
    
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)

model = load_model()

# ===============================
# 3. F1 STYLING (CSS MAGIC) 🎨
# ===============================
st.markdown("""
<style>
    /* 1. IMPORT FONTS */
    /* Titillium Web for Headings (The F1 Look) */
    @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@900&display=swap');
    /* Roboto for Body Text (Clean Readability) */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* 2. GLOBAL SETTINGS */
    .main {
        background-color: #f8f9fa;
    }
    
    /* 3. F1 STYLE HEADINGS */
    h1, h2, h3 {
        font-family: 'Titillium Web', sans-serif !important;
        text-transform: uppercase;
        font-style: italic; /* The Racing Tilt */
        letter-spacing: 1px;
    }
    
    h1 {
        color: #E10600; /* F1 Official Red */
        font-weight: 900;
        font-size: 3.5rem !important;
        text-shadow: 2px 2px 0px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #15151e; /* Dark Carbon */
        font-weight: 900;
        border-bottom: 3px solid #E10600; /* Red Underline */
        display: inline-block;
        padding-bottom: 5px;
    }
    
    h3 {
        color: #333;
        font-weight: 700;
    }
    
    /* 4. BODY TEXT */
    p, label, li, .stMarkdown, .stText {
        font-family: 'Roboto', sans-serif;
        color: #333333;
        font-size: 1.1rem;
    }
    
    /* 5. METRIC CARDS (Stats) */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-left: 6px solid #E10600; /* Red Racing Stripe */
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        transition: transform 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }
    div[data-testid="stMetricLabel"] {
        font-family: 'Titillium Web', sans-serif;
        font-weight: bold;
        text-transform: uppercase;
        color: #666;
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Titillium Web', sans-serif;
        font-weight: 900;
        font-size: 2rem !important;
        color: #15151e;
    }
    
    /* 6. BUTTONS (F1 Style) */
    div.stButton > button {
        background-color: #E10600;
        color: white;
        font-family: 'Titillium Web', sans-serif;
        font-weight: 900;
        font-style: italic;
        text-transform: uppercase;
        border-radius: 5px;
        border: none;
        padding: 0.6rem 2rem;
        font-size: 1.2rem;
        box-shadow: 0 4px 0px #b30500; /* 3D effect */
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #ff1a1a;
        transform: translateY(-2px);
        box-shadow: 0 6px 0px #b30500;
    }
    div.stButton > button:active {
        transform: translateY(2px);
        box-shadow: 0 0px 0px #b30500;
    }
    
    /* 7. SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #15151e; /* Dark F1 Theme */
    }
    section[data-testid="stSidebar"] * {
        color: #f0f0f0 !important;
        font-family: 'Titillium Web', sans-serif;
    }
    
    /* 8. ALERTS */
    .stSuccess {
        border-left: 5px solid #28a745;
    }
    .stError {
        border-left: 5px solid #dc3545;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# 4. SIDEBAR NAVIGATION
# ===============================
# You can use an F1 logo URL or local image if you have one
st.sidebar.title("🏎️ ANALYTICS HUB")
page = st.sidebar.radio(
    "MENU", 
    ["🏠 Home", "🔮 Predict Season", "🆚 Driver Comparison", "🧠 Model Insights", "🎮 Simulator", "🛠️ Tech Stack"]
)

st.sidebar.markdown("---")
st.sidebar.info("Developed by **Totz** 🚀")

# ===============================
# PAGE: HOME
# ===============================
if page == "🏠 Home":
    st.title("FORMULA 1 AI PREDICTOR")
    st.markdown("### THE FUTURE OF RACE STRATEGY")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
        Welcome to the ultimate F1 analytics dashboard. This tool leverages **Machine Learning (XGBoost)** to analyze historical data from 2010-2024 and predict future World Champions.
        
        **🚀 AVAILABLE MODULES:**
        * **Predict 2025:** Upload season stats to get real-time championship probabilities.
        * **Driver Comparison:** Head-to-head statistical face-off.
        * **AI Insights:** Understand the logic behind the predictions.
        * **Simulator:** Create your own "What-If" scenarios.
        """)
        st.success("👉 **GET STARTED:** Select **'Predict Season'** from the sidebar.")
    
    with col2:
        # Dummy chart for visual appeal on Home
        dummy_data = pd.DataFrame({
            'Driver': ['VER', 'NOR', 'HAM', 'LEC', 'PIA'],
            'Win Probability': [45, 30, 15, 8, 2]
        })
        st.bar_chart(dummy_data.set_index('Driver'), color="#E10600")
        st.caption("AI Model Probability Distribution (Sample)")

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
                    # Prediction Logic
                    features = ["points", "wins", "podiums"]
                    probs = model.predict_proba(df[features])[:, 1]
                    df["Win Probability"] = probs
                    df["Win Probability %"] = (probs * 100).round(2)
                    
                    # Store in session state for Comparison Page
                    st.session_state['f1_data'] = df
                    
                    # Highlight Winner
                    winner = df.loc[df["Win Probability"].idxmax()]
                    
                    st.success("Analysis Complete!")
                    st.divider()
                    
                    # Winner Highlight Section
                    col_main, col_chart = st.columns([1, 1.5])
                    
                    with col_main:
                        st.markdown("### 🏆 PREDICTED CHAMPION")
                        st.markdown(f"<h1 style='color: #E10600; font-style: italic;'>{winner['driver']}</h1>", unsafe_allow_html=True)
                        st.markdown(f"## {winner['team']}")
                        st.metric("CHAMPIONSHIP PROBABILITY", f"{winner['Win Probability %']}%", delta="Highest Odds")
                        
                        st.markdown("#### SEASON STATS")
                        c1, c2 = st.columns(2)
                        c1.metric("POINTS", winner['points'])
                        c1.metric("WINS", winner['wins'])
                        c2.metric("PODIUMS", winner['podiums'])
                        
                    with col_chart:
                        st.markdown("### 📈 PROBABILITY CHART")
                        # Bar Chart of Top 10
                        chart_data = df.sort_values("Win Probability", ascending=False).head(10)
                        st.bar_chart(chart_data.set_index("driver")["Win Probability %"], color="#E10600")

                    # Data Table
                    st.divider()
                    st.markdown("### 📋 FULL LEADERBOARD")
                    st.dataframe(
                        df.sort_values("Win Probability", ascending=False)[["driver", "team", "points", "wins", "podiums", "Win Probability %"]],
                        use_container_width=True
                    )
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
        with c1:
            d1_name = st.selectbox("SELECT DRIVER 1", drivers, index=0)
        with c2:
            d2_name = st.selectbox("SELECT DRIVER 2", drivers, index=1)
            
        if d1_name and d2_name:
            d1 = df[df['driver'] == d1_name].iloc[0]
            d2 = df[df['driver'] == d2_name].iloc[0]
            
            st.divider()
            
            col_a, col_mid, col_b = st.columns([1, 0.2, 1])
            
            # Driver 1 Card
            with col_a:
                st.markdown(f"<h2 style='text-align: center; color: #E10600;'>{d1['driver']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{d1['team']}</h3>", unsafe_allow_html=True)
                st.metric("WIN PROBABILITY", f"{d1['Win Probability %']}%")
                
            # VS Text
            with col_mid:
                st.markdown("<h1 style='text-align: center; font-size: 50px; color: #ccc;'>VS</h1>", unsafe_allow_html=True)
                
            # Driver 2 Card
            with col_b:
                st.markdown(f"<h2 style='text-align: center; color: #15151e;'>{d2['driver']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center;'>{d2['team']}</h3>", unsafe_allow_html=True)
                st.metric("WIN PROBABILITY", f"{d2['Win Probability %']}%")

            st.markdown("### 📊 STAT BREAKDOWN")
            
            # Comparison Dataframe
            comp_df = pd.DataFrame({
                'METRIC': ['TOTAL POINTS', 'RACE WINS', 'PODIUMS'],
                d1['driver']: [d1['points'], d1['wins'], d1['podiums']],
                d2['driver']: [d2['points'], d2['wins'], d2['podiums']]
            }).set_index('METRIC')
            
            st.table(comp_df)
            
            # AI Verdict
            st.markdown("### 🤖 AI VERDICT")
            if d1['Win Probability'] > d2['Win Probability']:
                st.success(f"**{d1['driver']}** has a statistically higher chance of winning based on superior consistency and win count.")
            elif d2['Win Probability'] > d1['Win Probability']:
                st.success(f"**{d2['driver']}** leads the prediction model with stronger season performance.")
            else:
                st.info("It's a dead heat! Both drivers have identical championship probabilities.")

# ===============================
# PAGE: MODEL INSIGHTS
# ===============================
elif page == "🧠 Model Insights":
    st.title("INSIDE THE AI MIND")
    st.write("Understand which statistics the XGBoost model values most.")
    
    if model:
        # Get Feature Importances
        try:
            importance = model.feature_importances_
            features = ["POINTS", "WINS", "PODIUMS"]
            
            imp_df = pd.DataFrame({
                'Feature': features,
                'Importance': importance
            }).sort_values(by='Importance', ascending=False)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### FEATURE IMPORTANCE CHART")
                st.bar_chart(imp_df.set_index("Feature"), color="#E10600")
                
            with col2:
                st.markdown("### KEY TAKEAWAYS")
                top_feature = imp_df.iloc[0]['Feature']
                st.info(f"🔹 **{top_feature}** is the #1 predictor.")
                st.write("This means the AI prioritizes this stat above all else when deciding a champion.")
                
        except:
            st.error("Feature importance unavailable for this model.")
    else:
        st.warning("Model not loaded.")

# ===============================
# PAGE: SIMULATOR
# ===============================
elif page == "🎮 Simulator":
    st.title("WHAT-IF SIMULATOR")
    st.write("Adjust stats to see how they impact championship odds in real-time.")
    
    # Styled Input Section
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
        
        with col_gauge:
             st.metric("WIN PROBABILITY", f"{prob:.2f}%")
        
        with col_text:
            if prob > 80:
                st.success("🏆 **DOMINANT CHAMPION!** These stats guarantee a title.")
            elif prob > 50:
                st.warning("🔥 **STRONG CONTENDER.** A very close fight for the title.")
            elif prob > 20:
                st.info("🏎️ **MID-FIELD.** Good season, but not championship material.")
            else:
                st.error("❌ **NO CHANCE.** Needs significantly better results.")

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
