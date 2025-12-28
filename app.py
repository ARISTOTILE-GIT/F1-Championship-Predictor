import streamlit as st
import pandas as pd
import joblib
import os

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="F1 Predictor by Totz",
    page_icon="🏎️",
    layout="wide"
)

# ===============================
# LOAD MODEL (ROOT DIRECTORY SAFE)
# ===============================
@st.cache_resource
def load_model():
    # This gets the folder where app.py is located (Root)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "f1_champion_predictor.pkl")

    if not os.path.exists(model_path):
        st.error(f"❌ Model file not found at: {model_path}")
        st.warning("Please make sure 'f1_champion_predictor.pkl' is uploaded to the GitHub repository.")
        st.stop()

    return joblib.load(model_path)

# Load the model
model = load_model()

# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("🏎️ F1 Predictor")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Predict from File", "Custom Prediction", "Tech Stack", "About"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Built by **Totz** 🚀")

# ===============================
# HOME
# ===============================
if page == "Home":
    st.markdown("## 🏁 Formula 1 Championship Predictor")
    st.markdown(
        "A clean AI-powered dashboard to predict the **Formula 1 World Champion** "
        "using season performance statistics."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 Upload season data")
    with col2:
        st.info("🤖 AI probability model")
    with col3:
        st.info("🏆 Champion prediction")

    st.markdown("---")
    st.success("👉 Go to **Predict from File** in the sidebar to start!")

# ===============================
# PREDICT FROM FILE
# ===============================
elif page == "Predict from File":
    st.markdown("## 📂 Upload Season CSV")
    st.caption("Required columns: driver, team, points, wins, podiums")

    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            required_cols = ["driver", "team", "points", "wins", "podiums"]
            if not all(col in df.columns for col in required_cols):
                st.error(f"CSV must contain these columns: {required_cols}")
            else:
                features = ["points", "wins", "podiums"]
                # Predict Probabilities
                probs = model.predict_proba(df[features])[:, 1]
                df["Win Probability (%)"] = probs * 100

                # Find Winner
                winner = df.loc[df["Win Probability (%)"].idxmax()]

                st.markdown("---")
                st.markdown("## 🏆 Predicted Champion")

                col1, col2, col3 = st.columns(3)
                col1.metric("Driver", winner["driver"])
                col2.metric("Team", winner["team"])
                col3.metric(
                    "Win Probability",
                    f"{winner['Win Probability (%)']:.2f}%"
                )
                
                if winner["Win Probability (%)"] > 50:
                    st.balloons()

                st.markdown("---")
                st.markdown("### 🏁 Championship Standings")

                st.dataframe(
                    df.sort_values("Win Probability (%)", ascending=False),
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Error reading file: {e}")

    else:
        st.info("Waiting for CSV upload...")

# ===============================
# CUSTOM PREDICTION
# ===============================
elif page == "Custom Prediction":
    st.markdown("## 🎮 Custom Season Prediction")
    st.write("Enter stats to see if you have what it takes to win!")

    col1, col2, col3 = st.columns(3)

    with col1:
        points = st.number_input("Points", 0.0, 600.0, 350.0)
    with col2:
        wins = st.slider("Wins", 0, 25, 5)
    with col3:
        podiums = st.slider("Podiums", 0, 25, 12)

    if st.button("Predict Outcome"):
        input_df = pd.DataFrame(
            [[points, wins, podiums]],
            columns=["points", "wins", "podiums"]
        )

        prob = model.predict_proba(input_df)[0][1]

        st.markdown("---")
        if prob > 0.15:
            st.success(f"🏆 Champion Potential! Win Probability: **{prob:.2%}**")
            st.balloons()
        else:
            st.error(f"❌ Not enough to win. Win Probability: **{prob:.2%}**")

# ===============================
# TECH STACK
# ===============================
elif page == "Tech Stack":
    st.markdown("## 🛠️ Tech Stack")
    st.markdown("""
    - **Python**: Core Language
    - **Streamlit**: Web Interface
    - **XGBoost**: Machine Learning Model
    - **Scikit-learn**: Data Processing
    - **Pandas**: Data Analysis
    """)

# ===============================
# ABOUT
# ===============================
elif page == "About":
    st.markdown("## ℹ️ About")
    st.markdown(
        "This AI project predicts Formula 1 championship outcomes "
        "using historical driver performance data from **2010–2024**."
    )
    st.markdown("**Developed by Totz** 🚀")

# ===============================
# FOOTER
# ===============================
st.markdown(
    """
    <div style="position: fixed; bottom: 0; width: 100%; text-align: center; color: grey; padding: 10px; background-color: white;">
        F1 Predictor Project | Developed by Totz
    </div>
    """,
    unsafe_allow_html=True
)
