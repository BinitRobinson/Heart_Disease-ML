import streamlit as st
import pandas as pd
import joblib

# Load saved model, scaler, and expected columns
model = joblib.load("KNN_heart_disease_model.pkl")
scaler = joblib.load("scaler.pkl")
expected_columns = joblib.load("columns.pkl")

st.set_page_config(page_title="Heart Disease Predictor", page_icon="❤️")

st.title("❤️ Heart Disease Prediction")
st.markdown("Provide the following details to check your heart disease risk:")

# Patient Name
name = st.text_input("👤 Enter Patient Name")

# Collect user input
col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 100, 40)
    sex = st.selectbox("Sex", ["Male", "Female"])
    chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])
    resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)
    cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1])

with col2:
    resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
    max_hr = st.slider("Max Heart Rate", 60, 220, 150)
    exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"])
    oldpeak = st.slider("Oldpeak (ST Depression)", -3.0, 6.0, 1.0)
    st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

# Predict Button
if st.button("🔍 Predict", use_container_width=True):

    if name.strip() == "":
        st.warning("⚠️ Please enter patient name")
    else:

        # Build base row
        input_dict = {col: 0 for col in expected_columns}

        # Numeric features
        input_dict['Age'] = age
        input_dict['RestingBP'] = resting_bp
        input_dict['Cholesterol'] = cholesterol
        input_dict['FastingBS'] = fasting_bs
        input_dict['MaxHR'] = max_hr
        input_dict['Oldpeak'] = oldpeak

        # One-hot encoding
        if sex == "Male" and "Sex_M" in input_dict:
            input_dict["Sex_M"] = 1

        if chest_pain != "ASY":
            col_name = f"ChestPainType_{chest_pain}"
            if col_name in input_dict:
                input_dict[col_name] = 1

        if resting_ecg != "LVH":
            col_name = f"RestingECG_{resting_ecg}"
            if col_name in input_dict:
                input_dict[col_name] = 1

        if exercise_angina == "Y" and "ExerciseAngina_Y" in input_dict:
            input_dict["ExerciseAngina_Y"] = 1

        if st_slope != "Down":
            col_name = f"ST_Slope_{st_slope}"
            if col_name in input_dict:
                input_dict[col_name] = 1

        # DataFrame
        input_df = pd.DataFrame([input_dict])[expected_columns]

        # Scale & predict
        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)[0]
        prob = model.predict_proba(scaled_input)[0][1]

        # ---------- OUTPUT ----------
        st.divider()
        st.subheader(f"🧾 Report for {name}")

        st.write(f"**Risk Probability:** {prob:.2f}")

        # ---------- FIXED RISK LOGIC ----------
        if prediction == 1:
            if prob >= 0.75:
                st.error("🚨 High Risk of Heart Disease")
                risk_level = "High"
            else:
                st.warning("⚠️ Moderate Risk of Heart Disease")
                risk_level = "Moderate"
        else:
            if prob >= 0.4:
                st.warning("⚠️ Moderate Risk of Heart Disease")
                risk_level = "Moderate"
            else:
                st.success("✅ Low Risk of Heart Disease")
                risk_level = "Low"

        # Progress bar
        st.progress(float(prob))

        # ---------- CLEAN PATIENT DETAILS ----------
        with st.expander("📋 Patient Details"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Name:** {name}")
                st.write(f"**Age:** {age}")
                st.write(f"**Sex:** {sex}")
                st.write(f"**Chest Pain:** {chest_pain}")
                st.write(f"**Resting BP:** {resting_bp}")

            with col2:
                st.write(f"**Cholesterol:** {cholesterol}")
                st.write(f"**Fasting BS:** {fasting_bs}")
                st.write(f"**Max HR:** {max_hr}")
                st.write(f"**Oldpeak:** {oldpeak}")
                st.write(f"**ST Slope:** {st_slope}")