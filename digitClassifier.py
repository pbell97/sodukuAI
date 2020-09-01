import cv2
import imutils
import numpy as np
import time
from matplotlib import pyplot as plt
from keras.models import load_model
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib
import copy


class DigitClassifierNN:
    def __init__(self):
        self.model = None
        self.class_names = []

    def trainNewModel(self, pathToImages):
        data_dir = pathToImages
        batch_size = 32
        img_height = 100
        img_width = 100
        train_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            batch_size=batch_size,
            image_size=(img_height, img_width)
        )
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size
        )
        self.class_names = train_ds.class_names

        # Caches for performance
        AUTOTUNE = tf.data.experimental.AUTOTUNE
        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

        # Creating the NN
        model = Sequential([
            layers.experimental.preprocessing.Rescaling(
                1./255, input_shape=(img_height, img_width, 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(len(self.class_names))
        ])

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(
                          from_logits=True),
                      metrics=['accuracy'])

        epochs = 2
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )

        self.model = model

    def saveModel(self, directory, modelName):
        self.model.save(os.path.join(path, modelName))

    def loadModel(self, pathToModel):
        self.model = tf.keras.models.load_model(pathToModel)
        self.class_names = ['1', '2', '3', '4',
                            '5', '6', '7', '8', '9', 'blank']

    def predict(self, image):
        # Temporary path to save image
        tempImagePath = os.path.join(os.getcwd(), "testImg.png")
        resizedCell = cv2.resize(
            image, (100, 100), interpolation=cv2.INTER_AREA)
        image = PIL.Image.fromarray(resizedCell)
        image = ImageOps.grayscale(image)
        image.save(tempImagePath)
        image = keras.preprocessing.image.load_img(
            tempImagePath, target_size=(100, 100)
        )

        # Deletes temporary image
        os.remove(tempImagePath)

        img_array = keras.preprocessing.image.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)  # Create a batch
        predictions = self.model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        prediction = self.class_names[np.argmax(score)]
        return prediction, np.max(score)
