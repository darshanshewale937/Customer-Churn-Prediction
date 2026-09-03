from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Churn Command Center", page_icon="📊", layout="wide")
MODEL_PATH = Path(__file__).parent.parent / "models" / "churn_model.joblib"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


model = load_model()

st.markdown("""<style>
.block-container {max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem;}
.hero {padding: 1.8rem 2rem; border-radius: 18px; background: linear-gradient(120deg,#102a43,#1d4ed8 58%,#0891b2); color:white; margin-bottom:1.25rem;}
.hero h1 {font-size:2.2rem; margin:0;}.hero p {font-size:1.05rem; margin:.45rem 0 0; opacity:.9;}
.metric-card {border:1px solid rgba(148,163,184,.35); border-radius:14px; padding:.85rem 1rem; min-height:80px;}
.metric-label {font-size:.8rem; opacity:.72; margin-bottom:.25rem;}.metric-value {font-size:1.2rem; font-weight:700;}
.result-card {border-radius:16px; padding:1.3rem 1.5rem; border-left:6px solid #22c55e; background:rgba(34,197,94,.10);}
.result-card.high {border-left-color:#ef4444; background:rgba(239,68,68,.10);}.result-card.medium {border-left-color:#f59e0b; background:rgba(245,158,11,.10);}
.result-title {font-size:1.45rem; font-weight:700; margin:0;}.result-copy {margin:.3rem 0 0; opacity:.85;}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.header("About this demo")
    st.write("A decision-support prototype for prioritising retention outreach.")
    st.divider()
    st.caption("MODEL"); st.write("Logistic Regression")
    st.caption("VALIDATION ROC-AUC"); st.write("84.21%")
    st.caption("DATASET"); st.write("IBM Telco Customer Churn")
    st.divider()
    st.info("Use this result to support retention decisions, not as an automated final decision.")

st.markdown("""<div class="hero"><h1>Customer Churn Command Center</h1><p>Turn customer profile data into a retention priority and recommended next action.</p></div>""", unsafe_allow_html=True)

for column, label, value in zip(st.columns(3), ["MODEL", "VALIDATION ROC-AUC", "CUSTOMERS ANALYSED"], ["Logistic Regression", "84.21%", "7,043"]):
    column.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

st.write("")
st.subheader("Customer profile")
st.caption("Complete the fields below, then generate a retention-risk assessment.")

with st.form("churn_form"):
    profile_tab, services_tab, billing_tab = st.tabs(["1. Customer", "2. Services", "3. Billing"])
    with profile_tab:
        left, right = st.columns(2)
        with left:
            gender = st.selectbox("Gender", ["Female", "Male"])
            senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
            partner = st.selectbox("Has Partner", ["No", "Yes"])
        with right:
            dependents = st.selectbox("Has Dependents", ["No", "Yes"])
            tenure = st.number_input("Tenure (months)", 0, 72, 12)
            phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    with services_tab:
        left, right = st.columns(2)
        with left:
            multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
            internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
            online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
            online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
        with right:
            device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
            tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
            streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
            streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
    with billing_tab:
        left, right = st.columns(2)
        with left:
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
            payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
        with right:
            monthly_charges = st.number_input("Monthly Charges", 0.0, value=70.0)
            total_charges = st.number_input("Total Charges", 0.0, value=840.0)
    submitted = st.form_submit_button("Generate risk assessment", type="primary", use_container_width=True)


def retention_action(contract, payment_method, tech_support, probability):
    signals = []
    if contract == "Month-to-month": signals.append("month-to-month contract")
    if payment_method == "Electronic check": signals.append("electronic-check payment")
    if tech_support == "No": signals.append("no tech support")
    if probability >= .60:
        action = "Assign a retention specialist and offer a tailored contract incentive."
    elif contract == "Month-to-month":
        action = "Offer a one-year contract upgrade with a targeted discount."
    elif tech_support == "No":
        action = "Offer a complimentary tech-support trial to increase service value."
    else:
        action = "Monitor the customer and include them in the next engagement campaign."
    return signals, action


if submitted:
    input_data = pd.DataFrame([{"gender": gender, "SeniorCitizen": int(senior_citizen == "Yes"), "Partner": partner, "Dependents": dependents, "tenure": tenure, "PhoneService": phone_service, "MultipleLines": multiple_lines, "InternetService": internet_service, "OnlineSecurity": online_security, "OnlineBackup": online_backup, "DeviceProtection": device_protection, "TechSupport": tech_support, "StreamingTV": streaming_tv, "StreamingMovies": streaming_movies, "Contract": contract, "PaperlessBilling": paperless_billing, "PaymentMethod": payment_method, "MonthlyCharges": monthly_charges, "TotalCharges": total_charges}])
    churn_probability = model.predict_proba(input_data)[0][1]
    signals, action = retention_action(contract, payment_method, tech_support, churn_probability)
    risk, style, headline = ("High", "high", "Immediate retention priority") if churn_probability >= .60 else (("Medium", "medium", "Proactive outreach recommended") if churn_probability >= .30 else ("Low", "low", "Low current churn risk"))
    st.write(""); st.subheader("Retention assessment")
    result_col, detail_col = st.columns([1.05, 1])
    with result_col:
        st.markdown(f'<div class="result-card {style}"><p class="result-title">{headline}</p><p class="result-copy">Risk segment: <b>{risk}</b></p></div>', unsafe_allow_html=True)
        st.write(""); st.metric("Churn probability", f"{churn_probability:.1%}"); st.progress(int(churn_probability * 100))
    with detail_col:
        st.markdown("**Recommended action**"); st.write(action)
        st.markdown("**Business signals to review**")
        st.write(" • " + "\n • ".join(signals) if signals else "No priority business signal was identified from the selected fields.")
    with st.expander("View submitted customer data"):
        st.dataframe(input_data, use_container_width=True, hide_index=True)
