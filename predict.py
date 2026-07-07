# predict.py
import random

def predict_image(image):
    """
    Simulated prediction function for Streamlit Cloud.
    Since TensorFlow/MobileNetV2 cannot be installed,
    this function randomly assigns 'General' or 'Infectious'
    with a confidence score.
    """

    # Randomly choose a class
    classes = ["General", "Infectious"]
    predicted_class = random.choice(classes)

    # Generate random confidence values
    confidence = round(random.uniform(70, 99), 2)

    # Probabilities for both classes
    if predicted_class == "General":
        probabilities = [confidence / 100, (100 - confidence) / 100]
    else:
        probabilities = [(100 - confidence) / 100, confidence / 100]

    return predicted_class, confidence, probabilities

