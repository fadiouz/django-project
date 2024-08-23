import cv2
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model
from sklearn.preprocessing import normalize
from scipy.spatial.distance import euclidean

# Load VGG16 model pre-trained on ImageNet dataset
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    return image

def extract_features(image_path):
    image = preprocess_image(image_path)
    features = model.predict(image)
    features = normalize(features, axis=1)
    return features

def compute_similarity(features1, features2):
    distance = euclidean(features1, features2)
    return distance

# Load and preprocess images
features1 = extract_features('../Data Set/paper1.jpg')
features2 = extract_features('../Data Set/paper2.jpg')
features1 = features1.reshape(features1.shape[1])
features2 = features2.reshape(features2.shape[1])

# Compute similarity
similarity_score = compute_similarity(features1, features2)
print(f"Image similarity score (Euclidean distance): {similarity_score}")
