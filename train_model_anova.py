
import pandas as pd
import numpy as np
import pickle
import json
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
from imblearn.over_sampling import SMOTENC

MODEL_DIR = r"backend/models"
RANDOM_STATE = 42



SELECTED_FEATURES = [
    'ProductRelated', 
    'ProductRelated_Duration', 
    'ExitRates', 
    'PageValues', 
    'SpecialDay', 
    'Month', 
    'Returning_Visitor'
]

def train_and_export():
    print("Loading data...")
    if os.path.exists("online_shoppers_intention.csv"):
        df = pd.read_csv("online_shoppers_intention.csv")
    elif os.path.exists("../online_shoppers_intention.csv"): # Try parent
        df = pd.read_csv("../online_shoppers_intention.csv") 
    else:
        print("Error: Dataset not found. Searching...")
        return

    print("Preprocessing...")

    month_map = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
        'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
    }
    df['Month'] = df['Month'].map(month_map)
    df['Returning_Visitor'] = df['VisitorType'].apply(lambda x: 1 if x == 'Returning_Visitor' else 0)
    y = df['Revenue'].astype(int)
    X = df[SELECTED_FEATURES]
    X = X.fillna(0)
    
    print(f"Features selected: {X.columns.tolist()}")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=RANDOM_STATE)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # (SMOTENC)
    print("Balancing data with SMOTENC...")
    cat_indices = [5, 6] 
    smote = SMOTENC(categorical_features=cat_indices, random_state=RANDOM_STATE)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)

    print("Training Gradient Boosting Model...")
    model = GradientBoostingClassifier(random_state=RANDOM_STATE, learning_rate=0.1, max_depth=5, n_estimators=100)
    model.fit(X_train_balanced, y_train_balanced)
    score = model.score(X_test_scaled, y_test)
    print(f"Test Accuracy: {score:.4f}")

    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"ROC-AUC Score: {auc:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    print(f"Exporting to {MODEL_DIR}...")

    with open(os.path.join(MODEL_DIR, 'gb_model.pkl'), 'wb') as f:
        pickle.dump(model, f)

    with open(os.path.join(MODEL_DIR, 'scaler.pkl'), 'wb') as f:
        pickle.dump(scaler, f)
        
    # Save Config
    config = {
        'selected_features': SELECTED_FEATURES,
        'all_columns_order': SELECTED_FEATURES, 
        'categorical_cols': ['Month', 'Returning_Visitor'] 
    }
    with open(os.path.join(MODEL_DIR, 'model_config.json'), 'w') as f:
        json.dump(config, f, indent=4)
        
    print("Model Export Complete!")

if __name__ == "__main__":
    train_and_export()
