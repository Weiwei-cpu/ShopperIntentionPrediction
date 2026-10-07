# Shopper Conversion Scenario Simulator 🛒✨

An end-to-end Machine Learning web application that predicts online shoppers' purchasing intentions in real time and simulates behavioral marketing scenarios to maximize conversion rates.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![Vue 3](https://img.shields.io/badge/Vue-3.x-4FC08D.svg)
![TailwindCSS](https://img.shields.io/badge/Tailwind-3.x-38B2AC.svg)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.6+-F7931E.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📌 Overview & Business Value

In modern e-commerce, converting casual visitors into paying customers is essential. This project utilizes the **UCI Online Shoppers Purchasing Intention Dataset** (~12,330 sessions) to uncover critical behavioral drivers behind purchase decisions and provides a **real-time scenario simulator** for marketing teams.

### Key Capabilities:
- **Real-Time Probability Estimation**: Adjust session metrics (pages viewed, session duration, exit rate, visitor type, season) to immediately compute conversion probability.
- **Dynamic Customer Segmentation**: Automatically classifies shoppers into 4 actionable tiers with recommended marketing triggers:
  - 🟢 **Ready Buyer (>75%)**: High purchase intent &rarr; Fast checkout (No discount needed).
  - 🟡 **Hesitant Shopper (45% - 75%)**: High consideration &rarr; Offer targeted 10% coupon or free shipping.
  - ⚪ **Low Intent (20% - 45%)**: Browsing &rarr; Recommend trending best sellers.
  - ⚪ **Window Shopper (<20%)**: Casual visitor &rarr; Non-intrusive email capture popup.
- **Behavioral Driver Scoring**: Calculates Interest Score, Risk Index, and Perceived Value in real time.

---

## 🏗️ System Architecture

```
data_mining/
│
├── backend/                        # FastAPI REST API Backend
│   ├── models/                     # Serialized Model Artifacts
│   │   ├── gb_model.pkl            # Trained Gradient Boosting Model
│   │   ├── scaler.pkl              # Fitted StandardScaler
│   │   └── model_config.json       # Feature configuration & metadata
│   ├── main.py                     # API server & prediction endpoints
│   └── requirements.txt            # Python dependencies
│
├── frontend/                       # Interactive Vue 3 Client
│   └── data_mining/
│       ├── src/
│       │   ├── App.vue             # Main Dashboard & Scenario Controls
│       │   └── main.ts             # Application entry point
│       ├── package.json            # Node.js dependencies
│       └── vite.config.ts          # Vite build configuration
│
├── data_mining_project_fixed.ipynb # Jupyter Notebook (EDA, ANOVA, Modeling)
├── online_shoppers_intention.csv   # UCI Benchmark Dataset
├── train_model_anova.py            # Standalone Training & Export Script
├── run_project.bat                 # One-Click Launcher for Windows
└── README.md                       # Project Documentation
```

---

## 🔬 Data Mining & Machine Learning Pipeline

1. **Feature Selection (ANOVA)**:
   Extracted the top 7 statistically significant drivers of purchasing intention:
   - `ProductRelated`: Number of product pages visited
   - `ProductRelated_Duration`: Total time spent on product pages (seconds)
   - `ExitRates`: Percentage of pageviews that were the final session exit
   - `PageValues`: Google Analytics page value metric
   - `SpecialDay`: Closeness of browsing date to holidays/festivals
   - `Month`: Seasonality indicator (0–11)
   - `Returning_Visitor`: Binary flag for repeat vs. new visitors

2. **Handling Class Imbalance**:
   Applied **SMOTENC** (Synthetic Minority Over-sampling Technique for Nominal and Continuous features) to resolve severe class imbalance in shopping conversions (~84.5% non-revenue vs. 15.5% revenue).

3. **Classification Model**:
   Trained a **Gradient Boosting Classifier** optimized for ROC-AUC score, capturing complex non-linear feature interactions and high predictive precision.

---

## 🚀 Quick Start Guide

### Option 1: One-Click Launch (Windows)

Simply double-click the included batch launcher:
```bat
run_project.bat
```
This automatically boots both the FastAPI backend (`http://localhost:8000`) and the Vite development server (`http://localhost:5173`).

---

### Option 2: Manual Step-by-Step Start

#### 1. Start Backend API
```bash
cd backend

# (Optional) Create & activate virtual environment
python -m venv venv
venv\Scripts\activate       # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies & run server
pip install -r requirements.txt
python main.py
```
> API runs at `http://localhost:8000`. Interactive Swagger docs available at `http://localhost:8000/docs`.

#### 2. Start Frontend UI
Open a second terminal window:
```bash
cd frontend/data_mining

# Install dependencies & start dev server
npm install
npm run dev
```
> Open your browser and navigate to `http://localhost:5173`.

---

## 🛠️ Retraining the Model

To retrain the model and export updated serialized weights to `backend/models/`:
```bash
python train_model_anova.py
```

---

## 📦 Tech Stack

- **Data Science & ML**: Python 3.11+, Scikit-Learn, Imbalanced-Learn, Pandas, NumPy
- **Backend**: FastAPI, Uvicorn, Pydantic
- **Frontend**: Vue 3 (Composition API), Vite, Tailwind CSS, Axios

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.