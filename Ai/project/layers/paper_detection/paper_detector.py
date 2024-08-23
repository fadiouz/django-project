from tensorflow.keras.models import load_model
import cv2
import numpy as np
import matplotlib.pyplot as plt

class paper_checker:
    def __init__(self,model_path):
        self.model = load_model(model_path)
        self.img_cols = 300
        self.img_rows = 400
    # Function to preprocess image using OpenCV
    def preprocess_image(self, img_array):

        # Resize image to target size
        img_resized = cv2.resize(img_array, (self.img_cols, self.img_rows))
        # Convert BGR (OpenCV default) to RGB
        img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
        # Normalize the image array
        img_normalized = img_gray / 255.0

        img_expanded = np.expand_dims(img_normalized, axis=(0, -1))

        return img_expanded

    def predict(self ,image):
        # Preprocess the image
        img_array = self.preprocess_image(image)

        # Make prediction
        prediction = self.model.predict(img_array)

        predicted_class = np.argmax(prediction, axis=1)

        if predicted_class[0] == 1:
            return True
        else:
            return False
        # return predicted_class
    