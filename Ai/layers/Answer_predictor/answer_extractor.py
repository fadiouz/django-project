
from tensorflow.keras.models import load_model
import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class Answer_Extractor:
    def __init__(self,model_path):
        self.model = load_model(model_path)
        self.img_cols = 150
        self.img_rows = 50
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

        if predicted_class[0] == 0:
            return('A')
        elif predicted_class[0] == 1:
            return('B')
        elif predicted_class[0] == 2:
            return('C')
        elif predicted_class[0] == 3:
            return('D')
        elif predicted_class[0] == 4:
            return('E')  
        else:
            return('none')
 
    def lite_predict(self , image):
        img_array = self.preprocess_image(image)

        interpreter = tf.lite.Interpreter(model_path="models/check_answer_perdictor.tflite")
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Set the tensor to the input data
        interpreter.set_tensor(input_details[0]['index'], img_array)
        
        # Run inference
        interpreter.invoke()

        # Get the output data
        output_data = interpreter.get_tensor(output_details[0]['index'])
      
        predicted_class = np.argmax(output_data, axis=1)

        if predicted_class[0] == 0:
            return('A')
        elif predicted_class[0] == 1:
            return('B')
        elif predicted_class[0] == 2:
            return('C')
        elif predicted_class[0] == 3:
            return('D')
        elif predicted_class[0] == 4:
            return('E')  
        else:
            return('none')