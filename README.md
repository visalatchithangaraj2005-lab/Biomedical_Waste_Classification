# 🧪 CNN-Based Soft Infectious Biomedical Waste Classification System

## 📌 Overview

This project is a deep learning-based biomedical waste classification system that automatically classifies soft biomedical waste into two categories:

- 🟢 General Waste
- 🔴 Infectious Waste

The system uses a MobileNetV2 Convolutional Neural Network (CNN) model and provides an interactive Streamlit web application for real-time prediction.

---

## 🚀 Features

- ✅ MobileNetV2 Deep Learning Model
- ✅ Image Upload
- ✅ Webcam Capture
- ✅ Real-time Prediction
- ✅ Prediction Confidence Score
- ✅ Prediction Dashboard
- ✅ Prediction History (CSV)
- ✅ Download Prediction History
- ✅ Waste Description
- ✅ Disposal Instructions
- ✅ Biomedical Safety Tips
- ✅ English / Tamil Language Support
- ✅ Responsive Dark Theme UI

---

## 🛠 Technologies Used

- Python
- TensorFlow / Keras
- MobileNetV2
- Streamlit
- NumPy
- Pandas
- Matplotlib
- Pillow
- ReportLab

---

## 📂 Project Structure

```
Biomedical_waste_App/
│
├── Model/
│   └── mobilenetv2_waste_model.h5
│
├── history/
│   └── prediction_history.csv
│
├── images/
│   └── logo.png
│
├── app.py
├── predict.py
├── class_names.txt
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

The model was trained on a biomedical waste image dataset containing two classes:

- General Waste
- Infectious Waste

Images were resized to **224 × 224** before training.

---

## ▶️ How to Run

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

### Install Requirements

```bash
pip install -r requirements.txt
```

### Run Streamlit

```bash
streamlit run app.py
```

---

## 📸 Application Workflow

1. Upload or capture an image.
2. Click **Predict**.
3. The model classifies the waste.
4. Displays:
   - Prediction
   - Confidence
   - Dashboard
   - Waste Description
   - Disposal Instructions
   - Safety Tips
5. Saves prediction history.

---

## 🎯 Model

- Architecture: MobileNetV2
- Framework: TensorFlow/Keras
- Image Size: 224 × 224
- Output Classes: 2

---

## 👩‍💻 Developer

**Visalatchi T**

Biomedical Engineering Student

PSNA College of Engineering and Technology

---

## 📄 License

This project is developed for educational and academic purposes.
