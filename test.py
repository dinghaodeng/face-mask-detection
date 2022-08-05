import pandas as pd
import numpy as np
import cv2
import json
import os
import matplotlib.pyplot as plt
import random
import seaborn as sns
import tensorflow as tf
from keras.models import Sequential
from keras import optimizers
from keras import backend as K
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator

def adjust_gamma(image, gamma=1.0):
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) *
                        255 for i in np.arange(0, 256)])
        return cv2.LUT(image.astype(np.uint8), table.astype(np.uint8))

def checkForMask(imagePaths):
    cvNet = cv2.dnn.readNetFromCaffe("deploy.prototxt", "weights.caffemodel")
    model = tf.keras.models.load_model("saved_models/model-1.h5")
    img_size = 124
    gamma = 2.0
    fig = plt.figure(figsize=(14, 14))
    rows = 3
    cols = 2
    axes = []
    assign = {'0': 'Mask', '1': "No Mask"}
    for j, im in enumerate(imagePaths):
        image = cv2.imread(im, 1)
        image = adjust_gamma(image, gamma=gamma)
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(
            image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        cvNet.setInput(blob)
        detections = cvNet.forward()
        for i in range(0, detections.shape[2]):
            try:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                frame = image[startY:endY, startX:endX]
                confidence = detections[0, 0, i, 2]
                if confidence > 0.2:
                    im = cv2.resize(frame, (img_size, img_size))
                    im = np.array(im)/255.0
                    im = im.reshape(1, 124, 124, 3)
                    result = model.predict(im)
                    if result > 0.5:
                        label_Y = 1
                    else:
                        label_Y = 0
                    cv2.rectangle(image, (startX, startY),
                                (endX, endY), (0, 0, 255), 2)
                    cv2.putText(image, assign[str(
                        label_Y)], (startX, startY-10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (36, 255, 12), 2)

            except:pass
        axes.append(fig.add_subplot(rows, cols, j+1))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.grid(False)

    plt.show()