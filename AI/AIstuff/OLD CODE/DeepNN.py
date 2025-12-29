import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
import re

from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, classification_report


file = 'final_final_df.csv'
df = pd.read_csv(file)

# df['pri_domain'] = df['pri_domain'].fillna('[None]')
# df['root_domain'] = df['root_domain'].fillna('[None]')

print(df.info())


x = df.drop(columns=['label'])
y = df['label']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=64)


model = keras.Sequential([
    keras.layers.Dense(256, activation='relu', input_shape=(x_train.shape[1],)),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(1, activation='sigmoid')
])


model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))

y_pred = model.predict(x_test)
y_pred_binary = [1 if pred >= 0.5 else 0 for pred in y_pred]


print(classification_report(y_test, y_pred_binary))

model.save('phishing_detection_model')