# app.py
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from datetime import datetime
import os
from predict import predict_image   # lightweight version

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="Biomedical Waste Classification",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("---")
st.header("📊 Dashboard")

history_file = "history/prediction_history.csv"

if os.path.exists(history_file):
    history = pd.read_csv(history_file)
    if len(history) > 0:
        history["Confidence"] = (
            history["Confidence"].astype(str).str.replace("%", "", regex=False).astype(float)
        )
        total = len(history)
        general = len(history[history["Prediction"].str.lower() == "general"])
        infectious = len(history[history["Prediction"].str.lower() == "infectious"])
        avg = history["Confidence"].mean()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📂 Total", total)
        c2.metric("🟢 General", general)
        c3.metric("🔴 Infectious", infectious)
        c4.metric("🎯 Avg Confidence", f"{avg:.2f}%")
    else:
        st.info("No predictions available.")

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.image("images/logo.png", width=220)
st.sidebar.markdown("# Biomedical Waste")
st.sidebar.markdown("---")
st.sidebar.success("👩‍💻 Developed by")
st.sidebar.markdown("## Visalatchi T")
st.sidebar.markdown("Biomedical Engineering Student")
st.sidebar.markdown("---")
st.sidebar.info("🤖 Simulated AI Model")
st.sidebar.markdown("---")
st.sidebar.subheader("Waste Categories")
st.sidebar.write("🟢 General Waste\n\n🔴 Infectious Waste")
st.sidebar.markdown("---")
st.sidebar.subheader("Technologies")
st.sidebar.write("✔ Python\n\n✔ Streamlit\n\n✔ PIL\n\n✔ Matplotlib")

# -------------------------------------------------
# LANGUAGE SELECTION
# -------------------------------------------------
language = st.sidebar.selectbox("🌐 Select Language", ["English", "தமிழ்"])

if language == "English":
    st.title("🧪 Biomedical Waste Classification System")
    st.write("### Developed by Visalatchi T")
    st.write("This application classifies biomedical waste into:\n\n🟢 General Waste\n\n🔴 Infectious Waste\n\nusing a simulated AI model.")
else:
    st.title("🧪 தொற்று உயிரியல் மருத்துவக் கழிவு வகைப்படுத்தும் அமைப்பு")
    st.write("### உருவாக்கியவர்: Visalatchi T")
    st.write("இந்த செயலி உயிரியல் மருத்துவக் கழிவுகளை வகைப்படுத்துகிறது.\n\n🟢 பொதுக் கழிவு\n\n🔴 தொற்று கழிவு\n\nAI மாதிரியை பயன்படுத்துகிறது.")

# -------------------------------------------------
# IMAGE INPUT
# -------------------------------------------------
st.header("📷 Select Image Source")
input_method = st.radio("Choose Input Method", ["📁 Upload Image", "📷 Capture from Webcam"], horizontal=True)

image, image_name = None, ""
if input_method == "📁 Upload Image":
    uploaded_file = st.file_uploader("Upload Biomedical Waste Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_name = uploaded_file.name
else:
    camera_photo = st.camera_input("Take a Picture")
    if camera_photo is not None:
        image = Image.open(camera_photo)
        image_name = "Captured_Image.jpg"

# -------------------------------------------------
# IMAGE PREVIEW
# -------------------------------------------------
if image is not None:
    st.markdown("---")
    st.subheader("🖼 Uploaded Image")
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.image(image, caption=image_name, use_container_width=True)
    with col2:
        st.success("✅ Image Loaded Successfully")
        st.info("Ready for prediction.\n\nClick the **Predict** button below.")

# -------------------------------------------------
# PREDICTION
# -------------------------------------------------
predicted_class, confidence, probabilities = None, None, None
predict_btn = st.button("🔍 Predict", use_container_width=True)

if predict_btn:
    if image is None:
        st.warning("⚠ Please upload or capture an image first.")
    else:
        with st.spinner("🔄 Predicting..."):
            predicted_class, confidence, probabilities = predict_image(image)

            # Save Prediction History
            new_data = pd.DataFrame({
                "Date": [datetime.now().strftime("%d-%m-%Y")],
                "Time": [datetime.now().strftime("%H:%M:%S")],
                "Image": [image_name],
                "Prediction": [predicted_class],
                "Confidence": [f"{confidence:.2f}"]
            })
            if os.path.exists(history_file):
                history = pd.read_csv(history_file)
            else:
                history = pd.DataFrame(columns=["Date", "Time", "Image", "Prediction", "Confidence"])
            history = pd.concat([history, new_data], ignore_index=True)
            history.to_csv(history_file, index=False)

            # Translate prediction
            display_prediction = predicted_class
            if language == "தமிழ்":
                if predicted_class.lower() == "general":
                    display_prediction = "பொதுக் கழிவு"
                elif predicted_class.lower() == "infectious":
                    display_prediction = "தொற்று கழிவு"

            # Display Prediction
            st.success(f"### Prediction : {display_prediction}")
            st.info(f"Confidence : {confidence:.2f}%")
# -------------------------------------------------
# Biomedical Waste Bin Recommendation
# -------------------------------------------------
if predicted_class is not None:
st.markdown("---")
st.subheader("🗑 Biomedical Waste Disposal Recommendation")

if predicted_class.lower() == "infectious":
    
    st.warning("""
### 🟡 Yellow Bin

**Waste Type:**
- Human tissues
- Blood contaminated materials
- Cotton
- Gauze
- Bandages
- Face Masks
- Gloves

**Treatment Method**
✔ Incineration
✔ Deep Burial
✔ Plasma Pyrolysis

⚠ Handle with PPE and dispose immediately.
""")

else:

    st.success("""
### 🟢 General Waste Bin

**Waste Type**
- Paper
- Plastic
- Food Waste
- Packaging
- Glass
- Cardboard

**Treatment Method**
✔ Recycling
✔ Municipal Waste Collection

♻ Segregate properly before disposal.
""")
    st.progress(confidence / 100)
    # -------------------------------------------------
# Confidence Level
# -------------------------------------------------

if confidence >= 95:
    st.success("🟢 Prediction Reliability : Very High")

elif confidence >= 85:
    st.success("🟢 Prediction Reliability : High")

elif confidence >= 70:
    st.warning("🟡 Prediction Reliability : Medium")

else:
    st.error("🔴 Prediction Reliability : Low")

# WASTE DESCRIPTION & DISPOSAL
# -------------------------------------------------
    st.markdown("---")
    st.subheader("📝 Waste Description")

    if predicted_class.lower() == "infectious":

        st.error("""
### 🔴 Infectious Biomedical Waste

Infectious biomedical waste contains materials contaminated with blood,
body fluids, microorganisms, bacteria, viruses, or other infectious agents.

#### Common Examples
- Used Gloves
- Face Masks
- Cotton
- Gauze
- Bandages
- Syringes (without needles)
- Blood-stained materials
- Dressings

#### Health Risks
- Spread of infectious diseases
- Cross-contamination
- Environmental pollution
- Risk to healthcare workers

#### Disposal Method
🟡 Dispose in the **Yellow Biomedical Waste Bin**
according to Biomedical Waste Management Rules.
""")

    else:

        st.success("""
### 🟢 General Biomedical Waste

General biomedical waste is non-infectious waste that does not contain
harmful microorganisms or hazardous biological materials.

#### Common Examples
- Paper
- Plastic Covers
- Food Waste
- Packaging Materials
- Glass Bottles
- Cardboard
- Clean Plastic Containers

#### Health Risks
- Low risk to humans
- Safe when segregated properly
- Recyclable in many cases

#### Disposal Method
🟢 Dispose in the **General Waste Bin**
and follow local muni
cipal waste management guidelines.
""")

# -------------------------------------------------
# SAFETY TIPS
# -------------------------------------------------
st.markdown("---")
st.subheader("🩺 Biomedical Safety Tips")
st.success("""
✔ Always wear gloves.
✔ Wash hands after handling biomedical waste.
✔ Do not mix infectious and general waste.
✔ Follow color-coded waste segregation.
✔ Dispose waste immediately after use.
✔ Use PPE whenever necessary.
""")

# -------------------------------------------------
# DOWNLOAD HISTORY
# -------------------------------------------------
st.markdown("---")
st.subheader("📥 Download Prediction History")

os.makedirs("history", exist_ok=True)
if not os.path.exists(history_file):
    empty_df = pd.DataFrame(columns=["Date", "Time", "Image", "Prediction", "Confidence"])
    empty_df.to_csv(history_file, index=False)

try:
    history = pd.read_csv(history_file)
    if history.empty:
        st.info("No prediction history available yet.")
    else:
        with open(history_file, "rb") as file:
            st.download_button(
                label="⬇️ Download Prediction History (CSV)",
                data=file,
                file_name="prediction_history.csv",
                mime="text/csv",
                use_container_width=True
            )
except Exception as e:
    st.error(f"Error loading prediction history: {e}")
        # -------------------------------------------------
# Generate PDF Report
# -------------------------------------------------

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

pdf_file = "Biomedical_Waste_Report.pdf"

doc = SimpleDocTemplate(pdf_file)

story = []

story.append(Paragraph("<b>Biomedical Waste Classification Report</b>", styles["Title"]))

story.append(Paragraph(f"<b>Date :</b> {datetime.now().strftime('%d-%m-%Y')}", styles["Normal"]))

story.append(Paragraph(f"<b>Time :</b> {datetime.now().strftime('%H:%M:%S')}", styles["Normal"]))

story.append(Paragraph(f"<b>Prediction :</b> {predicted_class}", styles["Normal"]))

story.append(Paragraph(f"<b>Confidence :</b> {confidence:.2f}%", styles["Normal"]))

if predicted_class.lower()=="infectious":
    disposal="Dispose in Yellow Biomedical Waste Bin"
else:
    disposal="Dispose in General Waste Bin"

story.append(Paragraph(f"<b>Disposal :</b> {disposal}", styles["Normal"]))

doc.build(story)

with open(pdf_file,"rb") as pdf:

    st.download_button(

        "📄 Download PDF Report",

        pdf,

        file_name="Biomedical_Waste_Report.pdf",

        mime="application/pdf"
    )



