import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from datetime import datetime
import os
from predict import predict_image   # lightweight version
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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

predicted_class = st.session_state.get("predicted_class", None)
confidence = st.session_state.get("confidence", 0)
probabilities = st.session_state.get("probabilities", None)

predict_btn = st.button("🔍 Predict", use_container_width=True)

if predict_btn:

    if image is None:

        st.warning("⚠ Please upload or capture an image first.")

    else:

        with st.spinner("🔄 Predicting..."):

            predicted_class, confidence, probabilities = predict_image(image)

            st.session_state.predicted_class = predicted_class
            st.session_state.confidence = confidence
            st.session_state.probabilities = probabilities

            # Save Prediction History
            os.makedirs("history", exist_ok=True)

            new_data = pd.DataFrame({
                "Date":[datetime.now().strftime("%d-%m-%Y")],
                "Time":[datetime.now().strftime("%H:%M:%S")],
                "Image":[image_name],
                "Prediction":[predicted_class],
                "Confidence":[f"{confidence:.2f}"]
            })

            if os.path.exists(history_file):
                history = pd.read_csv(history_file)
            else:
                history = pd.DataFrame(
                    columns=[
                        "Date",
                        "Time",
                        "Image",
                        "Prediction",
                        "Confidence"
                    ]
                )

            history = pd.concat([history,new_data],ignore_index=True)
            history.to_csv(history_file,index=False)

# Read values from Session State
predicted_class = st.session_state.predicted_class
confidence = st.session_state.confidence
probabilities = st.session_state.probabilities

# -------------------------------------------------
# DISPLAY PREDICTION
# -------------------------------------------------
predicted_class = st.session_state.get("predicted_class", None)
confidence = st.session_state.get("confidence", 0)
probabilities = st.session_state.get("probabilities", None)
if predicted_class is not None:

    display_prediction = predicted_class

    if language == "தமிழ்":

        if predicted_class.lower() == "general":
            display_prediction = "பொதுக் கழிவு"

        elif predicted_class.lower() == "infectious":
            display_prediction = "தொற்று கழிவு"

    st.markdown("---")
    st.subheader("🎯 Prediction Result")

    st.success(f"### Prediction : {display_prediction}")

    st.info(f"Confidence : {confidence:.2f}%")

    st.progress(confidence/100)
    # -------------------------------------------------
# Prediction Confidence Chart
# -------------------------------------------------
predicted_class = st.session_state.get("predicted_class", None)
confidence = st.session_state.get("confidence", 0)
probabilities = st.session_state.get("probabilities", None)
if probabilities is not None:

    st.markdown("---")
    st.subheader("📊 Prediction Confidence Chart")

    # Convert prediction probabilities to percentages
    scores = [float(x) * 100 for x in probabilities]

    labels = ["General", "Infectious"]

    fig, ax = plt.subplots(figsize=(6, 4))

    colors = ["green", "red"]

    bars = ax.bar(labels, scores, color=colors)

    ax.set_ylim(0, 100)
    ax.set_ylabel("Confidence (%)")
    ax.set_title("AI Prediction Confidence")

    # Display percentage above each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 2,
            f"{height:.2f}%",
            ha="center",
            fontsize=11
        )

    st.pyplot(fig)

else:
    st.warning("Prediction confidence is unavailable.")
    # -------------------------------------------------
# Prediction Reliability
# -------------------------------------------------
predicted_class = st.session_state.get("predicted_class", None)
confidence = st.session_state.get("confidence", 0)
probabilities = st.session_state.get("probabilities", None)
st.markdown("---")
st.subheader("🎯 Prediction Reliability")

if confidence >= 95:
    st.success("🟢 Very High Confidence")

elif confidence >= 85:
    st.success("🟢 High Confidence")

elif confidence >= 70:
    st.warning("🟡 Medium Confidence")

else:
    st.error("🔴 Low Confidence")
    # -------------------------------------------------
# Biomedical Waste Bin Recommendation
# -------------------------------------------------
predicted_class = st.session_state.get("predicted_class", None)
confidence = st.session_state.get("confidence", 0)
probabilities = st.session_state.get("probabilities", None)
if predicted_class is not None:

    st.markdown("---")
    st.subheader("🗑 Biomedical Waste Bin Recommendation")

    if predicted_class.lower() == "infectious":

        st.error("""
### 🟡 Yellow Biomedical Waste Bin

Dispose the waste in the **Yellow Biomedical Waste Bin**.

Examples:

• Gloves

• Face Mask

• Cotton

• Gauze

• Bandages

Treatment:

✔ Incineration

✔ Plasma Pyrolysis

✔ Deep Burial
""")

    elif predicted_class.lower() == "general":

        st.success("""
### 🟢 General Waste Bin

Dispose the waste in the **General Waste Bin**.

Examples:

• Paper

• Plastic

• Food Waste

• Glass

Treatment:

✔ Recycling

✔ Municipal Waste Collection
""")

else:

    st.info("Please predict an image first.")
    # -------------------------------------------------
# WASTE DESCRIPTION
# -------------------------------------------------
predicted_class = st.session_state.get("predicted_class", None)
confidence = st.session_state.get("confidence", 0)
probabilities = st.session_state.get("probabilities", None)

if predicted_class is not None:

    st.markdown("---")
    st.subheader("📝 Waste Description")

    if predicted_class.lower() == "infectious":

        st.error("""
### 🔴 Infectious Biomedical Waste

**Description**
Infectious biomedical waste contains materials contaminated with blood,
body fluids, microorganisms, bacteria, viruses, or other infectious agents.

#### Common Examples

• Used Gloves

• Face Masks

• Cotton

• Gauze

• Bandages

• Blood-Stained Dressings

#### Health Risks

• Spread of infectious diseases

• Cross-contamination

• Environmental pollution

• Risk to healthcare workers

#### Disposal Method
🟡 Dispose in the **Yellow Biomedical Waste Bin**
according to Biomedical Waste Management Rules.
""")

    elif predicted_class.lower() == "general":

        st.success("""
### 🟢 General Waste

**Description**
General waste is non-infectious waste that does not contain harmful biological materials.

#### Common Examples

• Paper

• Plastic Covers

• Food Waste

• Cardboard

• Glass Bottles

• Packaging Materials

#### Health Risks

• Low risk to humans

• Safe when segregated properly

• Recyclable in many cases

#### Disposal Method
🟢 Dispose in the **General Waste Bin**
and follow local waste management guidelines.
""")

    # -------------------------------------------------
# PDF REPORT DOWNLOAD
# -------------------------------------------------
predicted_class = st.session_state.get("predicted_class", None)
confidence = st.session_state.get("confidence", 0)
probabilities = st.session_state.get("probabilities", None)
if predicted_class is not None:

    st.markdown("---")
    st.subheader("📄 Download Prediction Report")

    styles = getSampleStyleSheet()

    pdf_file = "Biomedical_Waste_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    story = []

    story.append(
        Paragraph(
            "<b><font size=18>Biomedical Waste Classification Report</font></b>",
            styles["Title"],
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            f"<b>Date :</b> {datetime.now().strftime('%d-%m-%Y')}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Time :</b> {datetime.now().strftime('%H:%M:%S')}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Image :</b> {image_name}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Prediction :</b> {predicted_class}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Confidence :</b> {confidence:.2f}%",
            styles["Normal"],
        )
    )

    # Reliability
    if confidence >= 95:
        reliability = "Very High"

    elif confidence >= 85:
        reliability = "High"

    elif confidence >= 70:
        reliability = "Medium"

    else:
        reliability = "Low"

    story.append(
        Paragraph(
            f"<b>Prediction Reliability :</b> {reliability}",
            styles["Normal"],
        )
    )

    # Bin Recommendation
    if predicted_class.lower() == "infectious":

        bin_name = "Yellow Biomedical Waste Bin"

        treatment = "Incineration / Plasma Pyrolysis / Deep Burial"

    else:

        bin_name = "General Waste Bin"

        treatment = "Recycling / Municipal Waste Collection"

    story.append(
        Paragraph(
            f"<b>Recommended Bin :</b> {bin_name}",
            styles["Normal"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Treatment Method :</b> {treatment}",
            styles["Normal"],
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "<b>Biomedical Safety Tips</b>",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            """
• Wear gloves and PPE.<br/>
• Do not mix infectious and general waste.<br/>
• Dispose waste immediately.<br/>
• Follow Biomedical Waste Management Rules.<br/>
• Use color-coded bins correctly.
""",
            styles["Normal"],
        )
    )

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(
        Paragraph(
            "<b>Generated By</b><br/>"
            "Visalatchi T<br/>"
            "Biomedical Engineering Student<br/>"
            "Biomedical Waste Classification System",
            styles["Normal"],
        )
    )

    doc.build(story)

    with open(pdf_file, "rb") as pdf:

        st.download_button(
            "📥 Download PDF Report",
            data=pdf,
            file_name="Biomedical_Waste_Report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

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




