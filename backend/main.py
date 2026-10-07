
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
import os
import json
import traceback
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Shopper Conversion Scenario Simulator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fix path to be relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "gb_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
CONFIG_PATH = os.path.join(MODEL_DIR, "model_config.json")

model = None
scaler = None
config = {}

try:
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f: model = pickle.load(f)
    if os.path.exists(SCALER_PATH):
        with open(SCALER_PATH, "rb") as f: scaler = pickle.load(f)
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f: config = json.load(f)
except Exception as e:
    print(f"STARTUP ERROR: {e}")

class ScenarioInput(BaseModel):
    # This is the DIRECT ANOVA FEATURES
    product_related: int       
    product_related_duration: float 
    page_values: float         
    exit_rates: float          
    month: str
    is_special_day: bool
    is_returning_visitor: bool

@app.post("/predict")
def predict_scenario(data: ScenarioInput):
    if not model: return {"error": "Model not loaded properly. Check startup logs."}

    try:
        # Feature Selection
        f = {}
        f["ProductRelated"] = data.product_related
        f["ProductRelated_Duration"] = data.product_related_duration
        f["PageValues"] = data.page_values      
        f["ExitRates"] = data.exit_rates
        f["SpecialDay"] = 0.8 if data.is_special_day else 0.0
        f["Returning_Visitor"] = 1 if data.is_returning_visitor else 0
        
        month_map = {
            'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
            'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
        }
        f["Month"] = month_map.get(data.month, 10) 

        ordered_features = ['ProductRelated', 'ProductRelated_Duration', 'ExitRates', 'PageValues', 'SpecialDay', 'Month', 'Returning_Visitor']
        
        vector = []
        for feat in ordered_features:
            vector.append(f.get(feat, 0))            
        vector_np = np.array([vector])
        X_scaled = scaler.transform(vector_np)
        
        prob = model.predict_proba(X_scaled)[0][1]

        if prob > 0.75:
            segment = "Ready Buyer"
            color = "green"
            action = "Fast Checkout (No Coupon)"
        elif prob > 0.45:
            segment = "Hesitant Shopper"
            color = "yellow"
            action = "Offer 10% Discount"
        elif prob > 0.20:
            segment = "Low Intent"
            color = "gray"
            action = "Show Best Sellers"
        else:
            segment = "Window Shopper"
            color = "gray"
            action = "Capture Email"

        interest_score = min(100, (f["ProductRelated"] * 1.5) + (f["PageValues"] * 1.5))
        risk_score = min(100, (f["ExitRates"] / 0.2) * 100)
        
        return {
            "probability_percent": round(prob * 100, 1),
            "segment": segment,
            "segment_color": color,
            "recommended_action": action,
            "simulated_metrics": {
                "pages_viewed": int(f["ProductRelated"]),
                "avg_time": round(f["ProductRelated_Duration"] / max(1, f["ProductRelated"]), 1)
            },
            "analysis_drivers": {
                "interest": int(interest_score),
                "risk": int(risk_score),
                "value_score": int(min(100, f["PageValues"] * 2))
            }
        }

    except Exception as e:
        print(f"Prediction Error: {e}")
        return {"error": str(e), "trace": traceback.format_exc()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
