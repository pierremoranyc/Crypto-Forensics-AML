# 🛡️ CryptoGuard: Bitcoin Anti-Money Laundering (AML) AI

## 🚨 Project Overview
Money laundering in cryptocurrency is a massive challenge. This tool uses **Machine Learning (Ensemble Methods)** to detect illicit Bitcoin transactions based on the **Elliptic Data Set**. 

The system analyzes anonymized transaction features to flag high-risk activity with **75% Recall**, significantly reducing the manual workload for forensic investigators.

## 🧠 Model Architecture
* **Data:** 200,000+ Bitcoin transactions (Elliptic Dataset).
* **Strategy:** Temporal Split (Train on Past, Test on Future) to simulate real-world "Concept Drift."
* **Algorithm:** Voting Ensemble (Random Forest + XGBoost).
* **Performance:**
    * **Recall:** 74.3% (Capture Rate)
    * **Precision:** 57.6% (Trustworthiness)

## 💻 How to Run Locally
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run the App: `streamlit run src/app.py`

## 📊 Key Findings
* Fraud patterns evolve over time (Concept Drift observed).
* Specific features (V46, V90) serve as "Smoking Guns" for illicit activity.