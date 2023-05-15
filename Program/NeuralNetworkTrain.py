# -*- coding: utf-8 -*-

"""
Created on Thu Mar 23 19:11:48 2023

@author: pbori
"""
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, LSTM, Reshape
from sklearn.model_selection import train_test_split

categories = ['alfa', 'beta', 'gama'] 
label_map = {category: index for index, category in enumerate(categories)}
data = []
labels = []
for category in categories:
    folder = f"PrepearedData/{category}"                 #Adresa trénovacích dat
    for file in os.listdir(folder):
        if file.endswith('.txt'):
            path = os.path.join(folder, file)
            array = np.loadtxt(path)
            data.append(array)
            labels.append(label_map[category])
            if (len(array)!=256 or len(array[0])!=256):
                print("SIZE")

data = np.array(data)
labels = np.array(labels)  
Labels1 = to_categorical(labels)
train_data, test_data, train_labels, test_labels = train_test_split(data, Labels1, test_size=0.2)

model = Sequential([
    Conv2D(32, (5, 5), activation='relu', input_shape=(256, 256, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(128, activation='relu'),
    #Reshape((1, 128)),
    #LSTM(32),
    Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(train_data.reshape((-1, 256, 256, 1)), train_labels, epochs=10, batch_size=32)
Loss, Accurac = model.evaluate(test_data.reshape((-1, 256, 256, 1)), test_labels)
print(f"Loss: {Loss}")
print(f"Accuracy: {Accurac}")

Name="Model3_"+str(round(float(Loss),5))[2:]+".h5"
model.save(Name)


