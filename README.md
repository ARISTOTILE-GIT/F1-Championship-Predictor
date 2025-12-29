# 🏎️ F1 Championship Predictor

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![XGBoost](https://img.shields.io/badge/AI-XGBoost-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

### 🚀 The Ultimate AI-Powered Formula 1 Analytics Dashboard

This application uses **Machine Learning (XGBoost)** to analyze historical Formula 1 driver statistics (2010–2024) and predict the probability of winning the World Championship. It features a custom **"F1 Theme" UI**, real-time simulations, and head-to-head driver comparisons.

---

## 📸 Screenshots

| **Home Page** | **Season Prediction** |
|:---:|:---:|
| ![Home](https://github.com/user-attachments/assets/placeholder-home.png) | ![Prediction](https://github.com/user-attachments/assets/placeholder-predict.png) |
| *Clean UI with F1 Fonts* | *Probability Charts & Stats* |

| **Driver Comparison** | **What-If Simulator** |
|:---:|:---:|
| ![Compare](https://github.com/user-attachments/assets/placeholder-compare.png) | ![Simulator](https://github.com/user-attachments/assets/placeholder-sim.png) |
| *Head-to-Head Analysis* | *Real-time Championship Odds* |

*(Note: Replace the placeholder links above with your actual screenshot URLs after uploading images to your repo)*

---

## 🌟 Key Features

### 1. 🔮 Season Winner Prediction
* Upload a season dataset (CSV) containing driver stats.
* The AI predicts the **Champion** with a percentage probability score.
* Displays a **Leaderboard** and **Probability Bar Chart**.

### 2. 🆚 Head-to-Head Driver Comparison
* Select any two drivers from the dataset.
* Compare their **Points, Wins, and Podiums** side-by-side.
* AI generates a verdict on who has the statistical edge.

### 3. 🎮 Championship Simulator (What-If Analysis)
* An interactive tool to test custom scenarios.
* **Adjust sliders** for Points, Race Wins, and Podiums.
* See how small performance changes impact the title chances in real-time.

---

## ⚙️ How It Works

1.  **Data Collection:** Historical data from 2010 to 2024 (Hybrid Era focus).
2.  **Feature Engineering:** Key metrics used: `Total Points`, `Race Wins`, `Podiums`.
3.  **Model Training:** Trained using **XGBoost Classifier**, optimized for probability estimation.
4.  **UI/UX:** Built with **Streamlit**, featuring custom CSS for a "Light F1 Theme" (Titillium Web font, Custom Widgets).

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Custom CSS styling)
* **Machine Learning:** [XGBoost](https://xgboost.readthedocs.io/)
* **Data Processing:** [Pandas](https://pandas.pydata.org/)
* **Language:** Python 3.x

---

## 💻 Installation & Usage

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/f1-predictor.git](https://github.com/your-username/f1-predictor.git)
cd f1-predictor
