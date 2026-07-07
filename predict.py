import numpy as np
from import load_model
from PIL import Image

# Load model
model = load_model("Model/mobilenetv2_waste_model.keras")

# Load class names
with open("class_names.txt") as f:
    class_names = [line.strip() for line in f]


def predict_image(image):

    image = image.convert("RGB")
    image = image.resize((224,224))

    image = np.array(image)/255.0

    image = np.expand_dims(image,0)

    prediction = model.predict(image, verbose=0)

    predicted_index = np.argmax(prediction)

    predicted_class = class_names[predicted_index]

    confidence = float(np.max(prediction)*100)

    return predicted_class, confidence, prediction[0]
