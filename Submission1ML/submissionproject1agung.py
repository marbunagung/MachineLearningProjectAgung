# -*- coding: utf-8 -*-
"""SubmissionProject1Agung.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lu6GVAFOxjAEQ3N1fuH5yjt87nT2oUJQ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import nltk
import tensorflow as tf
nltk.download('punkt')

from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import word_tokenize

import warnings
warnings.filterwarnings('ignore')
sns.set()

df = pd.read_csv('IMDB Dataset.csv')
df.head()

df.tail()

"""Karena data mencapai 50000 saya hanya ingin menggunakan 5000 saja"""

df_subset = df.sample(n=5000, random_state=42)

df_subset

df_subset.info()

df_subset.sentiment.value_counts()

text = df_subset['review'][33553]
print(text)
print('<===============>')
print(word_tokenize(text))

corpus = []
for text in df_subset['review']:
  words = [word.lower() for word in word_tokenize(text)]
  corpus.append(words)

num_words = len(corpus)
print(num_words)

df_subset.shape

"""Disini saya tidak menggunakan metode sebagai berikut
from sklearn.model_selection import train_test_split
review_latih, review_test, label_latih, label_test = train_test_split(review, label, test_size=0.2)
"""

train_size = int(df_subset.shape[0] * 0.8)

review_latih = df_subset.review[:train_size]
review_test = df_subset.review[train_size:]

label_latih = df_subset.sentiment[:train_size]
label_test = df_subset.sentiment[train_size:]

tokenizer = Tokenizer(num_words)
tokenizer.fit_on_texts(review_latih)
review_latih = tokenizer.texts_to_sequences(review_latih)
review_latih = pad_sequences(review_latih, maxlen=128, truncating='post', padding='post')

review_latih[0], len(review_latih[0])

review_test = tokenizer.texts_to_sequences(review_test)
review_test = pad_sequences(review_test, maxlen=128, truncating='post', padding='post')

review_test[0], len(review_test[0])

le = LabelEncoder()
label_latih = le.fit_transform(label_latih)
label_test = le.transform(label_latih)

model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=50000, output_dim=100, input_length=128, trainable=True),
            tf.keras.layers.LSTM(100, dropout=0.1, return_sequences=True),
            tf.keras.layers.LSTM(100, dropout=0.1),
            tf.keras.layers.Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# berhubung hanya ingin membandingkan 2 value(nilai) ada baiknya menggunakan binary_crossentropy

from keras.layers import BatchNormalization

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=50000, output_dim=100, input_length=128, trainable=True),
    tf.keras.layers.LSTM(50, dropout=0.2, kernel_regularizer=tf.keras.regularizers.l2(0.01), return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(50, dropout=0.2, kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model.add(BatchNormalization())
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.9 and logs.get('val_accuracy')>0.9):
      self.model.stop_training = True
      print("\nAkurasi telah mencapai > 90%!")
callbacks = myCallback()

history = model.fit(review_latih, label_latih, epochs=20,
                    batch_size=64, validation_data=(review_latih, label_latih),
                    callbacks=[callbacks])

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()