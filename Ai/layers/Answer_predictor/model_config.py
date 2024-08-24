## Import required libraries 
import pandas as pd
import cv2
import numpy as np
import glob
import os
import random
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense ,Dropout
from sklearn.model_selection import train_test_split
from keras.preprocessing import image
from keras.utils import to_categorical
from sklearn.utils import shuffle
# from keras.preprocessing.image import ImageDataGenerator
# from keras.callbacks import ReduceLROnPlateau
# ##End import libraries


datasets = pd.read_csv('Ai/layers/Answer_predictor/Data Set/csv data/train.csv')
datasets = pd.concat([datasets ,datasets ,datasets,datasets,datasets])

# Encode classes
le = LabelEncoder()

datasets['class_name'] = le.fit_transform(datasets['class_name'])

train_data, test_data = train_test_split(datasets, test_size=0.1, random_state=42)

train_data = shuffle(train_data, random_state=42)
test_data = shuffle(test_data, random_state=42)


# Image dimensions
img_rows, img_cols = 50, 150

# Load and preprocess images
def load_and_preprocess_images(image_names, target_size=(img_rows, img_cols)):
    images = []
    for img_name in image_names:
        img_path = 'Ai/layers/Answer_predictor/Data Set/train data/' + str(img_name)  
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        images.append(gray_image)
        
    return np.array(images)



X_train = load_and_preprocess_images(train_data['image_name'])
X_test = load_and_preprocess_images(test_data['image_name'])


# Normalize pixel values to be between 0 and 1
X_train /= 255.0
X_test /= 255.0


# One-hot encode the target variable
Y_train = to_categorical(train_data['class_name'], num_classes=6)
Y_test = to_categorical(test_data['class_name'], num_classes=6)


X_train = X_train.reshape(-1,img_rows, img_cols,1)
X_test = X_test.reshape(-1,img_rows, img_cols,1)


print('shape of X_train', X_train.shape)
print('shape of Y_train', Y_train.shape)
print('shape of X_test', X_test.shape)
print('shape of Y_test', Y_test.shape)

idx = random.randint(0, len(X_train))

# print(idx)

# print(train_data.iloc[idx,:])

predicted_class = train_data.iloc[idx,:]['class_name']
# print(predicted_class)

if predicted_class == 0:
    plt.title('A')
elif predicted_class == 1:
    plt.title('B')
elif predicted_class == 2:
    plt.title('C')
elif predicted_class == 3:
    plt.title('D')
elif predicted_class == 4:
    plt.title('E')  
else:
    plt.title('none')
    
    
plt.imshow(X_train[idx, :], cmap='gray')
plt.show()



## Building the CNN Model
model = Sequential()

model.add(Conv2D(filters = 64, kernel_size = (4,4),padding = 'Same', 
                 activation ='relu', input_shape=(img_rows, img_cols, 1)))
model.add(MaxPooling2D(pool_size=(2,2),strides=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(filters = 32, kernel_size = (3,3),padding = 'Same', 
                 activation ='relu'))
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(filters = 16, kernel_size = (3,3),padding = 'Same', 
                 activation ='relu'))
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
model.add(Dropout(0.25))


model.add(Flatten())
model.add(Dense(64, activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(16, activation = "relu"))
model.add(Dropout(0.5))
model.add(Dense(6, activation = "softmax"))


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

model.fit(X_train, Y_train, epochs = 50, batch_size = 22)

accuracy = model.evaluate(X_test, Y_test)[1]
print(f'Model Accuracy: {accuracy * 100:.2f}%')


# Saving the Model
model.save('check_answer_perdictor.h5')



