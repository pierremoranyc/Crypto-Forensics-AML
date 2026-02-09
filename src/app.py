import streamlit as st
import joblib
import pandas as pd
import numpy as np

# --- 1. SETUP ---
st.set_page_config(page_title="CryptoGuard AI", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    div.stButton > button { width: 100%; background-color: #FF4B4B; color: white; height: 3em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. LOAD FILES ---
@st.cache_resource
def load_artifacts():
    try:
        model = joblib.load('fraud_model.pkl')
        features = joblib.load('top_features.pkl')
        feature_columns = joblib.load('feature_columns.pkl')
        return model, features, feature_columns
    except FileNotFoundError:
        return None, None, None

model, top_features, feature_columns = load_artifacts()

if model is None:
    st.error("🚨 Files missing. Please run the 'Master Save Block' in your Notebook.")
    st.stop()

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.title("👮‍♂️ Forensic Controls")

# [NEW] The "God Mode" Switch
# This forces the invisible features to be high-risk too
force_risk = st.sidebar.checkbox("⚠️ SIMULATE MASSIVE ATTACK", value=False)

st.sidebar.markdown("---")
input_data = {}

# If "Massive Attack" is on, we default sliders to 10.0, else -1.0 (Safe)
default_val = 10.0 if force_risk else -1.0

for feature in top_features:
    val = st.sidebar.slider(
        f"Feature {feature}",
        min_value=-5.0,
        max_value=50.0,
        value=default_val
    )
    input_data[feature] = val

# --- 4. MAIN DASHBOARD ---
st.title("🛡️ CryptoGuard AI")
st.caption("Forensic Analysis Dashboard")
st.markdown("---")

if st.button("🔍 SCAN TRANSACTION NOW"):
    
    # 1. Background Noise Logic
    # If "Massive Attack" is checked, we set the invisible 156 features to 10.0 (High Risk)
    # If unchecked, we set them to -1.0 (Safe)
    background_noise = 10.0 if force_risk else -1.0
    
    # Initialize ALL 166 columns with the background noise
    full_transaction = {col: background_noise for col in feature_columns}
    
    # 2. Overwrite the Top 10 with Slider Values
    for feature_name in top_features:
        full_transaction[feature_name] = input_data[feature_name]
    
    # 3. Create DataFrame & Fix Column Order
    df_input = pd.DataFrame([full_transaction])
    df_input = df_input[feature_columns] # Strict ordering
    
    # 4. Predict
    prediction = model.predict(df_input)[0]
    probability = model.predict_proba(df_input)[0][1]

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Verdict")
        if prediction == 1:
            st.error("🚨 FLAGGED: ILLICIT")
            st.image("https://media.giphy.com/media/l2Je3qSgD6Ipa9hQK/giphy.gif", width=300)
        else:
            st.success("✅ CLEARED: LICIT")
            st.image("https://media.giphy.com/media/3o7btQ8jDTPLAm6Wf6/giphy.gif", width=300)
            
    with col2:
        st.subheader("Confidence")
        st.metric("Fraud Probability", f"{probability:.2%}")
        st.progress(int(probability * 100))