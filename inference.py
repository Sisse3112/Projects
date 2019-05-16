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
save_dir = os.path.join('/content/gdrive/My Drive/CMPUT 206 Wi19/Lab10_Files/','saved')
model_name = 'keras_cifar10_trained_model_gray.h5' #change the name of the saved model accordingly

# The data, split between train and test sets:
_, (x_test, y_test) = cifar10.load_data()
print('x_test shape:', x_test.shape)
print(x_test.shape[0], 'test samples')

gray_test = np.empty((10000,32,32,1))
for i in range(10000):
  gray_test[i,:,:,0]=cv2.cvtColor(x_test[i,:,:,:],cv2.COLOR_BGR2GRAY)
x_test =gray_test


# Convert class vectors to binary class matrices.
y_test = keras.utils.to_categorical(y_test, num_classes)

model = load_model(os.path.join(save_dir,model_name))

x_test_copy = x_test.copy() #Make copy of the original images for displaying

x_test = x_test.astype('float32')
x_test = (x_test / 255)-0.5
x_test = x_test.astype('float32')

# Score trained model.
scores = model.evaluate(x_test, y_test, verbose=1)
print('Test accuracy:', scores[1])
y_predict=model.predict(x_test,verbose=1)
classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
samples_per_class = 7
for y, cls in enumerate(classes):
    idxs = np.flatnonzero (np.argmax(y_predict,axis=1)==np.argmax(y_test,axis=1))
    idxs = np.random.choice(idxs, samples_per_class, replace=False)
    for i, idx in enumerate(idxs):
        plt_idx = i * num_classes + y + 1
        plt.subplot(samples_per_class, num_classes, plt_idx)
        if x_test[idx].shape[-1] == 3:
            plt.imshow(x_test_copy[idx].squeeze().astype(np.uint8), cmap='gray') #change cmap='gray' when using gray input
        else:
            plt.imshow(x_test_copy[idx].squeeze().astype(np.uint8), cmap='gray')

        plt.axis('off')
        if i == 0:
            plt.title(cls)
plt.show()


 
