
from __future__ import print_function
import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
from keras.models import load_model

num_classes = 10
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'keras_cifar10_trained_model_color.h5' #change the name of the saved model accordingly

# The data, split between train and test sets:
_, (x_test, y_test) = cifar10.load_data()
print('x_test shape:', x_test.shape)
print(x_test.shape[0], 'test samples')

'''
#########################################################################
#                    WRITE YOUR CODE HERE                               #
# Convert images to Gray if your saved model is trained with gray       #
#########################################################################
'''

# Convert class vectors to binary class matrices.
y_test = keras.utils.to_categorical(y_test, num_classes)

model = load_model(os.path.join(save_dir,model_name))

x_test_copy = x_test.copy() #Make copy of the original images for displaying

'''
#########################################################################
#                    WRITE YOUR CODE HERE                               #
# Apply normalization if your saved model is trained with normalization #
#########################################################################
'''

x_test = x_test.astype('float32')

# Score trained model.
scores = model.evaluate(x_test, y_test, verbose=1)
print('Test accuracy:', scores[1])

'''
###################################################
#           WRITE YOUR CODE HERE                  #
# Show 7 misclassified samples for each class     #
# This time use model.predict instead, check wiki #
###################################################
'''

