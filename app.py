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
# 3. CSS STYLING (Clean Professional)
# ===============================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1f1f1f;
    }
    h1 { font-weight: 800; color: #E10600; } /* F1 Red */
    
    /* Button Styling */
    div.stButton > button {
        background-color: #E10600;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #b30500;
        color: white;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #15151e;
    }
    section[data-testid="stSidebar"] * {
        color: #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# 4. SIDEBAR NAVIGATION
# ===============================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg", width=100)
st.sidebar.title("Analytics Hub")
page = st.sidebar.radio(
    "Navigate", 
    ["🏠 Home", "🔮 Predict Season", "🆚 Driver Comparison", "🧠 Model Insights", "🎮 Simulator", "🛠️ Tech Stack"]
)

st.sidebar.markdown("---")
st.sidebar.info("Developed by **Totz** 🚀")

# ===============================
# PAGE: HOME
# ===============================
if page == "🏠 Home":
    st.title("🏎️ Formula 1 AI Analytics")
    st.markdown("### Welcome to the Next-Gen Prediction Engine")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        This tool uses **Machine Learning (XGBoost)** to analyze driver statistics and predict the World Champion.
        
        **Key Features:**
        * **Predict 2025:** Upload season data and get instant probabilities.
        * **Compare Drivers:** Head-to-head analysis of any two rivals.
        * **Explainability:** Understand *why* the AI chose the winner.
        * **Simulator:** Test your own "What-If" scenarios.
        """)
        st.info("👈 Start by selecting **'Predict Season'** in the sidebar.")
    
    with col2:
        # Placeholder chart for visual appeal
        dummy_data = pd.DataFrame({
            'Driver': ['Verstappen', 'Norris', 'Hamilton', 'Leclerc'],
            'Win Probability': [45, 35, 15, 5]
        })
        st.bar_chart(dummy_data.set_index('Driver'))
        st.caption("Sample Probability Distribution")

# ===============================
# PAGE: PREDICT SEASON
# ===============================
elif page == "🔮 Predict Season":
    st.title("📂 2025 Season Prediction")
    st.write("Upload the current season dataset to analyze championship odds.")
    
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
                    
                    st.success("✅ Analysis Complete!")
                    st.markdown("---")
                    
                    # Winner Highlight Section
                    col_main, col_chart = st.columns([1, 2])
                    
                    with col_main:
                        st.subheader("🏆 Predicted Champion")
                        st.markdown(f"<h1 style='font-size: 36px; margin:0;'>{winner['driver']}</h1>", unsafe_allow_html=True)
                        st.markdown(f"### {winner['team']}")
                        st.metric("Win Confidence", f"{winner['Win Probability %']}%", delta="Highest Probability")
                        
                        st.markdown("#### Key Stats:")
                        c1, c2 = st.columns(2)
                        c1.metric("Points", winner['points'])
                        c1.metric("Wins", winner['wins'])
                        c2.metric("Podiums", winner['podiums'])
                        
                    with col_chart:
                        st.subheader("📈 Championship Probability Chart")
                        # Bar Chart of Top 10
                        chart_data = df.sort_values("Win Probability", ascending=False).head(10)
                        st.bar_chart(chart_data.set_index("driver")["Win Probability %"], color="#E10600")

                    # Data Table
                    st.markdown("### 📋 Full Leaderboard")
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
    st.title("⚔️ Head-to-Head Comparison")
    
    if 'f1_data' not in st.session_state:
        st.warning("⚠️ Please upload a dataset in the **'Predict Season'** page first.")
    else:
        df = st.session_state['f1_data']
        drivers = df['driver'].unique()
        
        c1, c2 = st.columns(2)
        with c1:
            d1_name = st.selectbox("Select Driver 1", drivers, index=0)
        with c2:
            d2_name = st.selectbox("Select Driver 2", drivers, index=1)
            
        if d1_name and d2_name:
            d1 = df[df['driver'] == d1_name].iloc[0]
            d2 = df[df['driver'] == d2_name].iloc[0]
            
            st.markdown("---")
            
            col_a, col_mid, col_b = st.columns([1, 0.2, 1])
            
            # Driver 1 Card
            with col_a:
                st.markdown(f"<h2 style='text-align: center;'>{d1['driver']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: gray;'>{d1['team']}</p>", unsafe_allow_html=True)
                st.metric("Win Probability", f"{d1['Win Probability %']}%")
                st.progress(int(d1['Win Probability %']))
                
            # Comparison Stats
            with col_mid:
                st.markdown("<h3 style='text-align: center; margin-top: 100px;'>VS</h3>", unsafe_allow_html=True)
                
            # Driver 2 Card
            with col_b:
                st.markdown(f"<h2 style='text-align: center;'>{d2['driver']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center; color: gray;'>{d2['team']}</p>", unsafe_allow_html=True)
                st.metric("Win Probability", f"{d2['Win Probability %']}%")
                st.progress(int(d2['Win Probability %']))

            st.markdown("### 📊 Stat Breakdown")
            comp_df = pd.DataFrame({
                'Metric': ['Total Points', 'Race Wins', 'Podiums'],
                d1['driver']: [d1['points'], d1['wins'], d1['podiums']],
                d2['driver']: [d2['points'], d2['wins'], d2['podiums']]
            }).set_index('Metric')
            
            st.table(comp_df)
            
            # AI Verdict
            st.markdown("### 🤖 AI Verdict")
            if d1['Win Probability'] > d2['Win Probability']:
                st.success(f"The AI predicts **{d1['driver']}** has a higher chance of winning the title due to better consistency and win stats.")
            elif d2['Win Probability'] > d1['Win Probability']:
                st.success(f"The AI predicts **{d2['driver']}** has a stronger statistical advantage for the championship.")
            else:
                st.info("Both drivers have equal probability stats. It's a dead heat!")

# ===============================
# PAGE: MODEL INSIGHTS
# ===============================
elif page == "🧠 Model Insights":
    st.title("🧠 How the AI Thinks")
    st.write("Understand which statistics matter most to the Machine Learning model.")
    
    if model:
        # Get Feature Importances (Works for XGBoost/RandomForest)
        try:
            importance = model.feature_importances_
            features = ["Points", "Wins", "Podiums"]
            
            imp_df = pd.DataFrame({
                'Feature': features,
                'Importance': importance
            }).sort_values(by='Importance', ascending=False)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Feature Importance Chart")
                st.bar_chart(imp_df.set_index("Feature"))
                
            with col2:
                st.subheader("Key Takeaways")
                top_feature = imp_df.iloc[0]['Feature']
                st.info(f"🔹 **{top_feature}** is the most critical factor for predicting a champion.")
                st.write("This means the model prioritizes drivers who lead in this category over others.")
                
        except:
            st.error("Feature importance not available for this model type.")
    else:
        st.warning("Model not loaded.")

# ===============================
# PAGE: SIMULATOR
# ===============================
elif page == "🎮 Simulator":
    st.title("🎮 What-If Simulator")
    st.write("Adjust the sliders to see how stats affect winning probability in real-time.")
    
    c1, c2, c3 = st.columns(3)
    p_in = c1.number_input("Points", 0.0, 600.0, 350.0, step=10.0)
    w_in = c2.slider("Wins", 0, 25, 5)
    pod_in = c3.slider("Podiums", 0, 25, 10)
    
    if model:
        input_data = pd.DataFrame([[p_in, w_in, pod_in]], columns=["points", "wins", "podiums"])
        prob = model.predict_proba(input_data)[0][1] * 100
        
        st.markdown("---")
        st.subheader("Simulated Outcome")
        
        col_gauge, col_text = st.columns([1, 2])
        
        with col_gauge:
             st.metric("Win Probability", f"{prob:.2f}%")
        
        with col_text:
            if prob > 80:
                st.success("🏆 **Dominant Season!** Almost guaranteed champion.")
            elif prob > 50:
                st.warning("🔥 **Strong Contender!** Good chance, but needs consistency.")
            elif prob > 20:
                st.info("🏎️ **Mid-Field Battle.** Needs more wins to challenge for the title.")
            else:
                st.error("❌ **Not a Title Contender.**")

# ===============================
# PAGE: TECH STACK (NEW!)
# ===============================
elif page == "🛠️ Tech Stack":
    st.title("🛠️ Technology Stack")
    st.write("The modern tools and frameworks powering this AI application.")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Frontend & UI")
        st.info("**Streamlit**")
        st.write("Used for building the interactive web interface, charts, and sidebar navigation.")
        
        st.subheader("Machine Learning")
        st.error("**XGBoost**")
        st.write("The core Gradient Boosting algorithm used for high-accuracy championship prediction.")
        
    with col2:
        st.subheader("Data Processing")
        st.success("**Pandas**")
        st.write("Handles dataset manipulation, filtering, and feature engineering.")
        
        st.subheader("Backend Logic")
        st.warning("**Python**")
        st.write("The primary programming language connecting the UI, Data, and Model.")
        
    st.markdown("---")
    st.caption("F1 Championship Predictor | Developed by **Totz**")
